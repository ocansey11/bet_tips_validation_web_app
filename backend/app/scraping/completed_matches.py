# scraping/completed_standings.py
# Import Libraries and extras
import logging
from selenium import webdriver
import pandas as pd  # type: ignore
from sqlalchemy import create_engine
import re
from flask import g # type: ignore
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re



# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# CHROME DRIVER
def setup_chrome_driver():
    """Sets up the Chrome WebDriver."""
    logging.info("Setting up the Chrome WebDriver.")
    # Set up the Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Opens browser in full-screen
    driver = webdriver.Chrome(options=chrome_options)

    # Set the window size (optional, depends on your need)
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)

    # Open the Forebet predictions page for the English Premier League
    driver.get('https://www.forebet.com/en/football-tips-and-predictions-for-england/premier-league')

    # # Add a wait to ensure the element is present
    try:
        # Wait for the consent pop-up and click the consent button
        consent_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='fc-button-label' and text()='Consent']"))
        )
        consent_button.click()
        print("Clicked the consent button!")
    except Exception as e:
        print(f"Error: {e}")

    return driver

# SCRAPING DATA
def scrape_forebet_predictions(driver, url, className):
    """Scrapes data from Forebet's prediction page for completed matches."""
    logging.info(f"Accessing Forebet predictions page: {url}")

    driver.get(url)
    match_fixture_containers = driver.find_elements("class name", className)
    fixtures_container = [fixture.text for fixture in match_fixture_containers]
    driver.quit()

    logging.info("Successfully scraped data from Forebet.")
    return fixtures_container

# CLEANING DATA WITH REGEX
def clean_and_process_data(fixtures_container):
    """Cleans and processes scraped data."""
    logging.info("Starting data cleaning and processing.")
    
    # Getting the scraped data and separating the weekly round annot from the actual data
    matches_data_cleaned_step_1 = [match.split("\nEPL") for match in fixtures_container]
    epl_matches = matches_data_cleaned_step_1[0]

    # Extract weekly round from the first match's information
    cm_weekly_round = int(epl_matches[0].split(' ')[1]) - 1
    logging.info(f"Extracted weekly round: {cm_weekly_round}")

    # Extracting completed matches by using FT as indicator 
    completed_matches = [match for match in epl_matches if 'FT' in match]
    completed_matches = [match.replace('\nPRE\nVIEW', '') for match in completed_matches]

    # UPDATE REQUIRED HERE FOR REGEX
    # Preious version v1.
    # Regular expression pattern for matching completed matches data
    # pattern_completed_matches = r'\n(\d{2})(\d{2})(\d{2})([A-Z]|\d?)(\d?\s-\s\d{1})(\d{1}.\d{2})(\d{2}°|\d{1}°)(\d?.\d{2})\s(FT\s\d?\s-\s\d?)'
    # replacement_completed_matches = r'\n\1\n\2\n\3\n\4\n\5\n\6\n\7\n\8\n\9'

    # def replace_completed_matches(text):
    #     return re.sub(pattern_completed_matches, replacement_completed_matches, text)

    # Updated REGEX v2. This accounts for the fractional odds, as well as the decimal odds system
    def insert_zero_and_validate(number_string):
        # Convert the string into a list of integers
        digits = [int(digit) for digit in number_string]
        
        # Check different groupings by inserting '0' in each possible spot
        for i in range(1, len(digits)):
            # Create a new list with a '0' inserted at position i
            new_digits = digits[:i] + [0] + digits[i:]
            
            # Now we use static indices for the grouping
            # Group digits as: (index 0 and 1), (index 2 and 3), (index 4 and 5)
            first_group = int("".join(map(str, new_digits[:2])))  # 1st and 2nd digits
            second_group = int("".join(map(str, new_digits[2:4])))  # 3rd and 4th digits
            third_group = int("".join(map(str, new_digits[4:6])))  # 5th and 6th digits
            
            # Sum of the three groups
            total = first_group + second_group + third_group
            
            # Check if the total is close to 100 (with margin of error of 1)
            if abs(100 - total) <= 1:
                return "".join(map(str, new_digits))
        
        return "No valid grouping found"

    
    def extract_and_correct_probabilities(text):
        """
        This function extracts the probability portion of each match, corrects for any single digits, 
        and returns the updated probability string.
        """
        # Extract the portion before the dash
        prob_pattern = r'\n(\d+)\s-\s'  # Updated to capture 5 or 6 digit probabilities
        
        match = re.search(prob_pattern, text)
        if match:
            prob_str = match.group(1)  # The part containing probabilities
            
            if len(prob_str) < 8:
                # Handle the case where the probability string needs correction
                prob_str = prob_str[:-2]
                valid_probabilities = insert_zero_and_validate(prob_str)
                if valid_probabilities:
                    # Replace the old probability string with the corrected one
                    text = text.replace(prob_str, valid_probabilities)
        
        return text

    def fractional_to_decimal(fractional):
        """
        Converts fractional odds to decimal odds.
        Example: '11/10' -> 2.10
        """
        try:
            numerator, denominator = map(int, fractional.split('/'))
            return round((numerator / denominator) + 1, 2)
        except Exception as e:
            print(f"Error converting fractional odds: {e}")
            return fractional

    def replace_completed_matches(text):
        """
        This function applies the main regex to update the completed matches data.
        """
        def replacement_function(match):
            # Extract all groups from the regex
            group1 = match.group(1)
            group2 = match.group(2)
            group3 = match.group(3)
            group4 = match.group(4)
            group5 = match.group(5)
            group6 = match.group(6)
            group7 = match.group(7)
            decimal_odds = match.group(8)
            group9 = match.group(9)

            # If odds are in fractional format, convert them to decimal
            if '/' in decimal_odds:
                decimal_odds = fractional_to_decimal(decimal_odds)

            # Rebuild the string with updated decimal odds for the 8th group
            return f"\n{group1}\n{group2}\n{group3}\n{group4}\n{group5}\n{group6}\n{group7}\n{decimal_odds}\n{group9}"

        # Regular expression pattern for matching completed matches data, including both decimal and fractional odds.
        pattern_completed_matches = r'\n(\d{2})(\d{2})(\d{2})([A-Z]|\d?)(\d?\s-\s\d{1})(\d{1}.\d{2}|\d{1,2}\/\d{1,2})(\d{2}°|\d{1}°)(\d?.\d{2}|\d{1,2}\/\d{1,2})\s(FT\s\d?\s-\s\d?)'

        # Perform the replacement on the text
        return re.sub(pattern_completed_matches, replacement_function, text)


    # Step-by-step processing
    for i in range(len(completed_matches)):
        # Step 1: Correct probabilities
        completed_matches[i] = extract_and_correct_probabilities(completed_matches[i])
        
        # Step 2: Apply the main regex replacement
        completed_matches[i] = replace_completed_matches(completed_matches[i])


    # FINAL CLEANING AND PREPROCESSING.
    # Split data by /n to put them in required columns for pre processing
    completed_matches_split = [match.split('\n') for match in completed_matches]
    df_columns_completed_matches = ['', 'home', 'away', 'date_and_time', 'home_win_probability', 'draw_probability',
                                    'away_win_probability', 'team_to_win_prediction', 'scoreline_prediction',
                                    'average_goals_prediction', 'weather_in_degrees', 'odds', 'full_time_score',
                                    'score_at_halftime', "kelly_criterion"]
    df_completed_matches = pd.DataFrame(completed_matches_split, columns=df_columns_completed_matches)
    df_completed_matches = df_completed_matches.drop(columns=[''])
    logging.info("Data cleaning and processing completed.")
    return df_completed_matches, cm_weekly_round


# FEATURE ENGINEERING AND DATA PROCESSING
def prepare_data_for_modeling(df_completed_matches,cm_weekly_round,team_labels):
    """Prepares data for modeling."""
    logging.info("Preparing data for modeling.")
    
    def team_to_label(team_name):
        return team_labels.get(team_name)

    df_completed_matches['home'] = df_completed_matches['home'].map(team_to_label)
    df_completed_matches['away'] = df_completed_matches['away'].map(team_to_label)


    
    df_completed_matches[['date', 'time']] = df_completed_matches['date_and_time'].str.split(' ', expand=True)

    df_completed_matches[['home_team_score_prediction', 'away_team_score_prediction']] = \
    df_completed_matches['scoreline_prediction'].str.split('-', expand=True).astype(int)
    df_completed_matches.drop(columns=['scoreline_prediction'], inplace=True)

    df_completed_matches[['home_team_full_time_score', 'away_team_full_time_score']] = \
        df_completed_matches['full_time_score'].str.strip('FT ').str.split(' - ', expand=True).astype(int)
    
    df_completed_matches[['home_team_halftime_score', 'away_team_halftime_score']] = \
        df_completed_matches['score_at_halftime'].str.strip('()').str.split(' - ', expand=True)


    # Additional data processing steps...sigh
    def create_y(df):
        """
        Create the target variable (y) based on the prediction results.

        Args:
            df (DataFrame): The DataFrame containing match predictions and actual outcomes.

        Returns:
            list: The target variable (y) indicating whether the prediction was correct (1) or not (0)
        """
        y = []
        for i in range(len(df)):
            if df['team_to_win_prediction'][i] == '1' and df['home_team_full_time_score'][i] > df['away_team_full_time_score'][i]:
                y.append(1)
            elif df['team_to_win_prediction'][i] == '2' and df['home_team_full_time_score'][i] < df['away_team_full_time_score'][i]:
                y.append(1)
            elif df['team_to_win_prediction'][i] == 'X' and df['home_team_full_time_score'][i] == df['away_team_full_time_score'][i]:
                y.append(1)
            else:
                y.append(0)
        return y

    # Append the y column to the main DataFrame
    df_completed_matches['prediction_result'] = create_y(df_completed_matches)

    # Convert probabilities to float
    df_completed_matches['home_win_probability'] = df_completed_matches['home_win_probability'].astype(float)
    df_completed_matches['draw_probability'] = df_completed_matches['draw_probability'].astype(float)
    df_completed_matches['away_win_probability'] = df_completed_matches['away_win_probability'].astype(float)
    df_completed_matches['average_goals_prediction'] = df_completed_matches['average_goals_prediction'].astype(float)
    df_completed_matches['odds'] = df_completed_matches['odds'].astype(float)

    # Convert relevant score columns to integers
    df_completed_matches['home_team_full_time_score'] = df_completed_matches['home_team_full_time_score'].astype(int)
    df_completed_matches['away_team_full_time_score'] = df_completed_matches['away_team_full_time_score'].astype(int)
    df_completed_matches['home_team_halftime_score'] = df_completed_matches['home_team_halftime_score'].astype(int)
    df_completed_matches['away_team_halftime_score'] = df_completed_matches['away_team_halftime_score'].astype(int)

    #Drop columns 
    df_completed_matches.drop(columns=['kelly_criterion'], inplace=True)

    # Convert 'Date' column to datetime with correct format
    df_completed_matches['date'] = pd.to_datetime(df_completed_matches['date'], format='%d/%m/%Y')
    df_completed_matches['day_of_week'] = df_completed_matches['date'].dt.dayofweek
    df_completed_matches['month'] = df_completed_matches['date'].dt.month
    df_completed_matches['weekly_round'] = cm_weekly_round
    
    # Next season Chnages
    # df_completed_matches['date_and_time'] = pd.to_datetime(df_completed_matches['date_and_time'], format='%d/%m/%Y %H:%M')
    # Assuming the 'time' column is in the format '%H:%M' (24-hour clock)
    # df_completed_matches['time'] = pd.to_datetime(df_completed_matches['time'], format='%H:%M').dt.time
    

    # Custom label mapping
    label_mapping = {'X': 0, '1': 1, '2': 2}
    df_completed_matches['team_to_win_prediction'] = df_completed_matches['team_to_win_prediction'].map(label_mapping)
    logging.info("Custom label encoding for 'team_to_win_prediction' completed.")

    logging.info("Data preparation for modeling completed.")
    return df_completed_matches


# CREATING ENGINE AND INSERTING DATA INTO DB
def insert_data_into_database(df_completed_matches, db_url):
    """Inserts the cleaned data into the database."""
    logging.info("Inserting data into the database.")
    engine = create_engine(db_url)
    with engine.connect() as connection:
        df_completed_matches.to_sql('completed_matches', con=connection, if_exists='replace', index=False)
    logging.info("Data insertion completed.")


# MAIN SCRAPPER
def main(url, className, user, password, host, port, dbname,team_labels):
    driver = setup_chrome_driver()
    try:
        fixtures_container = scrape_forebet_predictions(driver, url, className)
        df_completed_matches, cm_weekly_round = clean_and_process_data(fixtures_container)
        df_completed_matches = prepare_data_for_modeling(df_completed_matches,cm_weekly_round,team_labels)
        db_url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'  
        insert_data_into_database(df_completed_matches, db_url)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
