# scraping/league_standings.py
# Import Libraries and extras
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd #type:ignore
from sqlalchemy import create_engine

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# CHROME DRIVER
def setup_driver():
    """Sets up the Chrome WebDriver."""
    logging.info("Setting up the Chrome WebDriver.")
    driver = webdriver.Chrome()
    return driver

# SCRAPING DATA
def extract_league_table(driver, url, className):
    """Scrapes data from SWofascore's prediction page for either pls or cls(previous|current league standings)."""
    logging.info(f"Accessing Forebet predictions page: {url}")
    driver.get(url)
    driver.set_window_size(1920, 1080)
    # driver.maximize_window()  
    league_table_results = driver.find_elements("class name", className)
    league_table_results_container = []

    logging.info("Successfully scraped data from Sofascore.")
    for results in league_table_results:
        results_text = results.text
        league_table_results_container.append(results_text)
    
    return league_table_results_container

# Function to process the raw data
def process_data(data):
    """Cleans and processes scraped data."""
    logging.info("Starting data cleaning and processing.")
    data_copy_split = data.split('\n')[1:] 

    # If the weekly round is less than 5. the last_5_matches column wont be very useful
    weekly_round = 1  # Update this value as needed for now its hard coded.

    # Calculate the slice length based on weekly_round. `points` is considered so ill add +1 for slice length
    slice_length = 7 + min(weekly_round, 5) + 1 

    # Split the data based on the calculated slice length
    data_array = [data_copy_split[i:i+slice_length] for i in range(0, len(data_copy_split), slice_length)]

    # UNCOMMENT THE CODE BELOW IF CODE ABOVE CAUSES ERROR
    # Cant remove this code completely. This worked when the last 5 matches was 5 or more
    # data_array = [data_copy_split[i:i+13] for i in range(0, len(data_copy_split), 13)]
    
    for data in data_array:
        data[6:7] = data[6].split(':')
    
    logging.info("Data cleaning and processing completed.")
    return data_array, slice_length

# POINTS PER GAME CALC
def calculate_ppg_and_create_last_5_matches(data_array, slice_length):
    """Calculates Points per Game using last_5_matches column"""
    logging.info("Calculating Points Per Game")
    for row in data_array:
        ppg = 0
        last_column = slice_length
        for result in row[7:last_column]:
            if result == 'W':
                ppg += 3
            elif result == 'D':
                ppg += 1
        last_5_matches = ''.join(row[8:13])
        row[8:13] = [last_5_matches, ppg / 5]
    
    logging.info("Points Per Game calculated")
    return data_array

# MAP TEAM LABELS
def team_to_label(team_name, team_labels):
    return team_labels.get(team_name)

# Function to create a DataFrame
def create_dataframe(data_array, columns, team_labels,slice_length):
    """Prepare cleaned Data for DB by creating a dataframe"""
    logging.info("Preparing data for database.")
    df_data = calculate_ppg_and_create_last_5_matches(data_array,slice_length)
    df = pd.DataFrame(df_data, columns=columns)
    df['team'] = df['team'].apply(lambda x: team_to_label(x, team_labels))
    # df = df.drop(columns=['last_5_matches'])
    
    return df

# MAIN SCRAPPER
def main( table_name,url,className, user,password,host,port,dbname,team_labels):
    driver = setup_driver()
    try:
        league_table_data = extract_league_table(driver, url, className)
        data = league_table_data[0][43:]  # The values before 43 represent the table info. column names etc from sofascore
        processed_data, slice_length = process_data(data)
        premier_league_columns = ['pos', 'team', 'pld', 'wins', 'draws', 'losses', 'gf', 'ga', 'last_5_matches', 'ppg_last_5_Matches', 'points']
        premier_league_table = create_dataframe(processed_data, premier_league_columns, team_labels,slice_length)
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}')
        premier_league_table.to_sql(table_name, con=engine, if_exists='replace', index=False)
        logging.info("Data insertion completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
