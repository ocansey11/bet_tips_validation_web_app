# scraping/completed_standings.py
# Import Libraries and extras
import logging
from selenium import webdriver
import pandas as pd  # type: ignore
from sqlalchemy import create_engine
import re
from flask import g # type: ignore



# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# CHROME DRIVER
def setup_chrome_driver():
    """Sets up the Chrome WebDriver."""
    logging.info("Setting up the Chrome WebDriver.")
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
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
    
    matches_data_cleaned_step_1 = [match.split("\nEPL") for match in fixtures_container]
    
    epl_matches = matches_data_cleaned_step_1[0]

    # Extract weekly round from the first match's information
    cm_weekly_round = int(epl_matches[0].split(' ')[1]) - 1
    logging.info(f"Extracted weekly round: {cm_weekly_round}")

    completed_matches = [match for match in epl_matches if 'FT' in match]
    completed_matches = [match.replace('\nPRE\nVIEW', '') for match in completed_matches]

    # Regular expression pattern for matching completed matches data
    pattern_completed_matches = r'\n(\d{2})(\d{2})(\d{2})([A-Z]|\d?)(\d?\s-\s\d{1})(\d{1}.\d{2})(\d{2}°|\d{1}°)(\d?.\d{2})\s(FT\s\d?\s-\s\d?)'
    replacement_completed_matches = r'\n\1\n\2\n\3\n\4\n\5\n\6\n\7\n\8\n\9'

    def replace_completed_matches(text):
        return re.sub(pattern_completed_matches, replacement_completed_matches, text)

    completed_matches = [replace_completed_matches(match) for match in completed_matches]
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

    df_completed_matches.drop(columns=['kelly_criterion'], inplace=True)

    # Convert 'Date' column to datetime with correct format
    df_completed_matches['date'] = pd.to_datetime(df_completed_matches['date'], format='%d/%m/%Y')
    df_completed_matches['day_of_week'] = df_completed_matches['date'].dt.dayofweek
    df_completed_matches['month'] = df_completed_matches['date'].dt.month
    df_completed_matches['weekly_round'] = cm_weekly_round
    

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
    # old way
    # engine = create_engine(db_url)
    # df_completed_matches.to_sql('completed_matches', con=engine, if_exists='replace', index=False)

    engine = create_engine(db_url)
    
    # Using connection directly
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
