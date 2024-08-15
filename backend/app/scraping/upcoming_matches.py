import logging
from selenium import webdriver
from sklearn.preprocessing import LabelEncoder  # type: ignore
from sqlalchemy import create_engine
import pandas as pd  # type: ignore
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# CHROME DRIVER
def setup_chrome_driver():
    logging.info("Setting up Chrome driver.")
    driver = webdriver.Chrome()
    return driver


# SCRAPING DATA
def scrape_upcoming_matches(driver, url, className):
    logging.info(f"Scraping upcoming matches from {url} with class name '{className}'.")
    driver.get(url)
    match_fixture_containers = driver.find_elements("class name", className)
    fixtures_container = [fixture.text for fixture in match_fixture_containers]

    driver.quit()
    return fixtures_container


# EXTRACTING WEEKLY ROUNDS NUMBER
def extract_metadata(fixtures_container):
    logging.info("Extracting metadata from fixtures.")
    matches_data_cleaned_step_1 = [match.split("\nEPL") for match in fixtures_container]
    epl_matches = matches_data_cleaned_step_1[0]
    um_weekly_round = epl_matches[0].split(' ')[-1]
    return um_weekly_round, epl_matches


# Preparing data for cleaning
def clean_data(epl_matches):
    logging.info("Cleaning match data.")
    upcoming_matches = [match for match in epl_matches if 'FT' not in match]
    upcoming_matches = upcoming_matches[1:]  # Assuming the first element is metadata
    upcoming_matches = [match.replace('\nPRE\nVIEW', '') for match in upcoming_matches]
    upcoming_matches = [re.sub(r'\nRound\s\d{1,2}', '', match) for match in upcoming_matches]
    return upcoming_matches


# CLEANING DATA WITH REGEX
def format_data(upcoming_matches):
    logging.info("Formatting match data.")
    pattern = r'\n(\d{2})(\d{2})(\d{2})([A-Z]|\d?)(\d?\s-\s\d{1})(\d{1}.\d{2})(\d{2}°|\d{1}°)(\d?.\d{2})'
    replacement = r'\n\1\n\2\n\3\n\4\n\5\n\6\n\7\n\8'

    def replace_upcoming_matches(text):
        return re.sub(pattern, replacement, text)

    upcoming_matches = [replace_upcoming_matches(match) for match in upcoming_matches]
    upcoming_matches_split = [match.split('\n') for match in upcoming_matches]
    df_columns_upcoming_matches = ['', 'home', 'away', 'date and time', 'home_win_probability', 'draw_probability', 'away_team_win_probability', 'team_to_win_prediction', 'scoreline_prediction', 'average_goals_prediction', 'weather_in_degrees', 'odds', "kelly_criterion"]
    df_upcoming_matches = pd.DataFrame(upcoming_matches_split, columns=df_columns_upcoming_matches)
    df_upcoming_matches = df_upcoming_matches.drop(columns=[''])
    return df_upcoming_matches

# PROCESSING DATA AND FEATURE ENGINEERING
def preprocess_data(df_upcoming_matches, um_weekly_round):
    logging.info("Preprocessing match data.")
    team_labels = {
        'Arsenal': 1, 'Aston Villa': 2, 'Bournemouth': 3, 'Brighton': 4, 'Burnley': 5, 'Chelsea': 6,
        'Crystal Palace': 7, 'Everton': 8, 'Fulham': 9, 'Leeds United': 10, 'Leicester City': 11,
        'Liverpool': 12, 'Manchester City': 13, 'Manchester United': 14, 'Newcastle United': 15,
        'Norwich City': 16, 'Sheffield United': 17, 'Southampton': 18, 'Tottenham': 19, 'West Ham': 20,
        'Luton Town': 21, 'Wolverhampton': 22, 'Brentford': 23, 'Nottingham Forest': 24
    }

    def team_to_label(team_name):
        return team_labels.get(team_name)

    df_upcoming_matches['home'] = df_upcoming_matches['home'].map(team_to_label)
    df_upcoming_matches['away'] = df_upcoming_matches['away'].map(team_to_label)
    df_upcoming_matches[['date', 'time']] = df_upcoming_matches['date and time'].str.split(' ', expand=True)
    df_upcoming_matches.drop(columns=['date and time'], inplace=True)
    df_upcoming_matches[['home_team_score_prediction', 'away_team_score_prediction']] = df_upcoming_matches['scoreline_prediction'].str.split('-', expand=True)
    df_upcoming_matches['home_team_score_prediction'] = df_upcoming_matches['home_team_score_prediction'].astype(int)
    df_upcoming_matches['away_team_score_prediction'] = df_upcoming_matches['away_team_score_prediction'].astype(int)
    df_upcoming_matches['home_win_probability'] = df_upcoming_matches['home_win_probability'].astype(float)
    df_upcoming_matches['draw_probability'] = df_upcoming_matches['draw_probability'].astype(float)
    df_upcoming_matches['away_win_probability'] = df_upcoming_matches['away_win_probability'].astype(float)
    df_upcoming_matches['average_goals_prediction'] = df_upcoming_matches['average_goals_prediction'].astype(float)
    df_upcoming_matches['odds'] = df_upcoming_matches['odds'].astype(float)
    df_upcoming_matches.drop(columns=['kelly_criterion'], inplace=True)
    df_upcoming_matches['date'] = pd.to_datetime(df_upcoming_matches['date'], format='%d/%m/%Y')
    df_upcoming_matches['day_of_week'] = df_upcoming_matches['date'].dt.dayofweek
    df_upcoming_matches['month'] = df_upcoming_matches['date'].dt.month
    df_upcoming_matches['weekly_round'] = um_weekly_round
    label_encoder = LabelEncoder()
    df_upcoming_matches['team_to_win_prediction'] = label_encoder.fit_transform(df_upcoming_matches['team_to_win_prediction'])
    return df_upcoming_matches


# SAVE TO DATABASE
def save_to_database(df_upcoming_matches, user, password, host, port, dbname):
    logging.info("Saving data to the database.")
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}')
    df_upcoming_matches.to_sql('upcoming_matches', con=engine, if_exists='replace', index=False)


# MAIN SCRAPER
def main(url, className, user, password, host, port, dbname):
    driver = setup_chrome_driver()
    try:
        fixtures_container = scrape_upcoming_matches(driver, url, className)
        um_weekly_round, epl_matches = extract_metadata(fixtures_container)
        upcoming_matches = clean_data(epl_matches)
        df_upcoming_matches = format_data(upcoming_matches)
        df_upcoming_matches = preprocess_data(df_upcoming_matches, um_weekly_round)
        save_to_database(df_upcoming_matches, user, password, host, port, dbname)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
