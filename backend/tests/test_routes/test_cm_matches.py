import pytest #type:ignore
from unittest.mock import patch, MagicMock
from flask import Flask #type:ignore
from flask.testing import FlaskClient #type:ignore
from app.routes import matches_bp
from app import create_app
import pandas as pd #type:ignore

@pytest.fixture
def client():
    app = create_app('testing')  # Assuming you have a testing config
    with app.test_client() as client:
        with app.app_context():
            # Set up any required database state here
            yield client
        # Teardown happens here automatically

@patch('app.scraping.cm_scrapper')
def test_completed_route(mock_cm_scrapper, client: FlaskClient):
    mock_cm_scrapper.return_value = None  # Mock the scraper function
    response = client.get('/matches/completed')

    assert response.status_code == 200
    assert response.get_json() == {'message': 'Scraping completed and data stored successfully'}

@patch('app.scraping.um_scrapper')
def test_upcoming_route(mock_um_scrapper, client: FlaskClient):
    mock_um_scrapper.return_value = None  # Mock the scraper function
    response = client.get('/matches/upcoming')

    assert response.status_code == 200
    assert response.get_json() == {'message': 'Scraping completed and data stored successfully'}

# Testing setup_chrome_driver
@patch('selenium.webdriver.Chrome')
def test_setup_chrome_driver(mock_chrome):
    driver = setup_chrome_driver()
    mock_chrome.assert_called_once()  # Ensures that the Chrome driver is called

# Testing scrape_forebet_predictions
@patch('selenium.webdriver.Chrome')
def test_scrape_forebet_predictions(mock_chrome):
    mock_driver = mock_chrome.return_value
    mock_driver.get.return_value = None  # Mock get method
    mock_driver.find_elements.return_value = [MagicMock(text='Mocked Content\nEPL')]

    url = 'http://mockurl.com'
    class_name = 'mockClass'

    results = scrape_forebet_predictions(mock_driver, url, class_name)
    assert results == ['Mocked Content\nEPL']

# Testing clean_and_process_data
def test_clean_and_process_data():
    sample_data = ['Mocked Content\nEPL']
    result_df = clean_and_process_data(sample_data)

    # Assert expected columns are present
    expected_columns = ['home', 'away', 'date', 'time', 'home_win_probability', 
                        'draw_probability', 'away_win_probability', 'team_to_win_prediction',
                        'average_goals_prediction', 'weather_in_degrees', 'odds', 'full_time_score',
                        'score_at_halftime', 'kelly_criterion']

    assert list(result_df.columns) == expected_columns
    # Additional assertions can be added here based on the expected data

# Testing insert_data_into_database
@patch('sqlalchemy.create_engine')
def test_insert_data_into_database(mock_create_engine):
    mock_engine = mock_create_engine.return_value
    mock_conn = mock_engine.connect.return_value.__enter__.return_value

    df_completed_matches = pd.DataFrame({
        'home': ['Team A'], 'away': ['Team B'], 'date': ['2024-08-14'], 'time': ['20:00'],
        'home_win_probability': [0.5], 'draw_probability': [0.3], 'away_win_probability': [0.2],
        'team_to_win_prediction': ['Team A'], 'average_goals_prediction': [2.5],
        'weather_in_degrees': [20], 'odds': [1.5], 'full_time_score': ['2-1'],
        'score_at_halftime': ['1-1'], 'kelly_criterion': [0.7]
    })

    insert_data_into_database(df_completed_matches, 'sqlite:///:memory:')
    mock_conn.execute.assert_called()  # Verify if insert is called