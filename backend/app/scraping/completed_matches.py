# Setup and Imports
from selenium import webdriver
import pandas as pd # type: ignore
from sqlalchemy import create_engine
import re
from sklearn.preprocessing import LabelEncoder # type: ignore

def setup_chrome_driver():
    """Sets up the Chrome WebDriver."""
    driver = webdriver.Chrome()
    return driver

def scrape_forebet_predictions(driver,url,className):
    """Scrapes data from Forebet's prediction page for completed matches."""
    # Open the Forebet predictions page for the English Premier League
    driver.get(url)
    match_fixture_containers = driver.find_elements("class name", className)
    
    fixtures_container = [fixture.text for fixture in match_fixture_containers]
    driver.quit()
    
    return fixtures_container

def clean_and_process_data(fixtures_container):
    """Cleans and processes scraped data."""
    matches_data_cleaned_step_1 = [match.split("\nEPL") for match in fixtures_container]
    epl_matches = matches_data_cleaned_step_1[0]

    weekly_round = int(epl_matches[0].split(' ')[1]) 

    completed_matches = [match for match in epl_matches if 'FT' in match]
    completed_matches = [match.replace('\nPRE\nVIEW', '') for match in completed_matches]

    # Regular expression pattern for matching completed matches data
    pattern_completed_matches = r'\n(\d{2})(\d{2})(\d{2})([A-Z]|\d?)(\d?\s-\s\d{1})(\d{1}.\d{2})(\d{2}°|\d{1}°)(\d?.\d{2})\s(FT\s\d?\s-\s\d?)'
    replacement_completed_matches = r'\n\1\n\2\n\3\n\4\n\5\n\6\n\7\n\8\n\9'

    def replace_completed_matches(text):
        return re.sub(pattern_completed_matches, replacement_completed_matches, text)

    completed_matches = [replace_completed_matches(match) for match in completed_matches]
    completed_matches_split = [match.split('\n') for match in completed_matches]

    df_columns_completed_matches = ['', 'home', 'away', 'date and time', 'home_win_probability', 'draw_probability',
                                    'away_win_probability', 'team_to_win_prediction', 'scoreline_prediction',
                                    'average_goals_prediction', 'weather_in_degrees', 'odds', 'full_time_score',
                                    'score_at_halftime', "kelly_criterion"]
    
    df_completed_matches = pd.DataFrame(completed_matches_split, columns=df_columns_completed_matches)
    df_completed_matches = df_completed_matches.drop(columns=[''])

    return df_completed_matches

def prepare_data_for_modeling(df_completed_matches):
    """Prepares data for modeling."""
    team_labels = {
        # Define team labels here...
    }

    def team_to_label(team_name):
        return team_labels.get(team_name)

    df_completed_matches['home'] = df_completed_matches['home'].map(team_to_label)
    df_completed_matches['away'] = df_completed_matches['away'].map(team_to_label)

    df_completed_matches[['date', 'time']] = df_completed_matches['date and time'].str.split(' ', expand=True)
    df_completed_matches.drop(columns=['date and time'], inplace=True)

    df_completed_matches[['home_team_score_prediction', 'away_team_score_prediction']] = \
        df_completed_matches['scoreline_prediction'].str.split('-', expand=True).astype(int)
    df_completed_matches.drop(columns=['scoreline_prediction'], inplace=True)

    df_completed_matches[['home_team_full_time_score', 'away_team_full_time_score']] = \
        df_completed_matches['full_time_score'].str.strip('FT ').str.split(' - ', expand=True).astype(int)

    # Additional data processing steps...

    return df_completed_matches

def insert_data_into_database(df_completed_matches, db_url):
    """Inserts the cleaned data into the database."""
    engine = create_engine(db_url)
    df_completed_matches.to_sql('completed_matches', con=engine, if_exists='append', index=False)

def main(url,className,user,password,host,port,dbname):
    driver = setup_chrome_driver()
    fixtures_container = scrape_forebet_predictions(driver,url,className)
    df_completed_matches = clean_and_process_data(fixtures_container)
    df_completed_matches = prepare_data_for_modeling(df_completed_matches)
    db_url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'  # Replace with actual DB credentials
    insert_data_into_database(df_completed_matches, db_url)

if __name__ == "__main__":
    main()
