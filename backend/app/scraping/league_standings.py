from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd #type:ignore
from sqlalchemy import create_engine


# Function to setup the Chrome WebDriver
def setup_driver():
    # Run in headless mode for faster performance
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  
    driver = webdriver.Chrome()
    return driver

# Function to extract league table data
def extract_league_table(driver, url, className):
    driver.get(url)
    driver.maximize_window()  # maximize window to ensure all elements are visible
    league_table_results = driver.find_elements("class name", className)
    league_table_results_container = []

    for results in league_table_results:
        results_text = results.text
        league_table_results_container.append(results_text)
    
    return league_table_results_container

# Function to process the raw data
def process_data(data):
    data_copy_split = data.split('\n')[1:]  # Skip the first line if it's a header
    data_array = [data_copy_split[i:i+13] for i in range(0, len(data_copy_split), 13)]
    
    for data in data_array:
        data[6:7] = data[6].split(':')
    
    return data_array

# Function to calculate points per game and create last 5 matches summary
def calculate_ppg_and_create_last_5_matches(data_array):
    for row in data_array:
        ppg = 0
        for result in row[7:13]:
            if result == 'W':
                ppg += 3
            elif result == 'D':
                ppg += 1
        last_5_matches = ''.join(row[8:13])
        row[8:13] = [last_5_matches, ppg / 5]
    
    return data_array

# Function to map team names to labels
def team_to_label(team_name, team_labels):
    return team_labels.get(team_name)

# Function to create a DataFrame
def create_dataframe(data_array, columns, team_labels):
    df_data = calculate_ppg_and_create_last_5_matches(data_array)
    df = pd.DataFrame(df_data, columns=columns)
    df['Team'] = df['Team'].apply(lambda x: team_to_label(x, team_labels))
    df = df.drop(columns=['Last 5 Matches'])
    return df

# Main Function
def main( table_name,url,className, user,password,host,port,dbname ):
    # Setup driver and URL
    driver = setup_driver()


    try:
        # Extracting Data
        league_table_data = extract_league_table(driver, url, className)
        data = league_table_data[0][43:]  # Adjust according to actual data layout

        # Processing Data
        processed_data = process_data(data)

        # Creating DataFrame
        premier_league_columns = ['Pos', 'Team', 'Pld', 'Wins', 'Draws', 'Losses', 'GF', 'GA', 'Last 5 Matches', 'Ppg_Last_5_Matches', 'Points']
        team_labels = {
            'Arsenal': 1, 'Aston Villa': 2, 'Bournemouth': 3, 'Brighton': 4, 'Burnley': 5,
            'Chelsea': 6, 'Crystal Palace': 7, 'Everton': 8, 'Fulham': 9, 'Leeds Utd': 10,
            'Leicester City': 11, 'Liverpool': 12, 'Man City': 13, 'Man Utd': 14, 'Newcastle': 15,
            'Norwich': 16, 'Sheffield': 17, 'Southampton': 18, 'Tottenham': 19, 'West Ham': 20,
            'Luton': 21, 'Wolves': 22, 'Brentford': 23, 'Sheffield Utd': 24, 'Forest': 25
        }
        premier_league_table = create_dataframe(processed_data, premier_league_columns, team_labels)

        # Database Connection and Insertion
       
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}')
        premier_league_table.to_sql(table_name, con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
