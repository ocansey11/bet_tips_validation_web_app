import pytest #type:ignore
from unittest.mock import patch, MagicMock
from flask import Flask #type:ignore
from flask.testing import FlaskClient #type:ignore
from app.routes import matches_bp
from app import create_app
from app.config import TestingConfig
import pandas as pd #type:ignore
from app.utils import db  
from app.scraping.upcoming_matches import setup_chrome_driver, scrape_upcoming_matches,clean_data
from app.scraping import  um_scrapper, url_forebet, forebet_className,user,password,host,port


@pytest.fixture
def app():
    """Fixture for setting up the Flask application for testing."""
    app = create_app(class_config=TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Fixture for setting up the Flask test client."""
    return app.test_client()

def test_setup_chrome_driver():
    """Test the setup of the Chrome WebDriver."""
    driver = setup_chrome_driver()
    assert driver is not None
    driver.quit()

def test_scrape_forebet_predictions():
    """Test the scraping function to fetch upcoming matches."""
    driver = setup_chrome_driver()
    url = url_forebet
    class_name = forebet_className

    results = scrape_upcoming_matches(driver, url, class_name)
    assert isinstance(results, list)
    assert len(results) > 0  # Ensure we have at least one match scraped
    driver.quit()


# Testing clean_and_process_data
def test_clean_data():
    # I have to supply my own mock data with Rou
    sample_data = ['Round 38\nEPL\nArsenal\nEverton\n19/5/2024 15:00\n53202713 - 13.1622°1.18 FT 2 - 1\n(1 - 1)\nEPL\nBrentford\nNewcastle United\n19/5/2024 15:00\n27254921 - 33.1322°2.20 FT 2 - 4\n(0 - 3)\n0.07\nEPL\nBrighton\nManchester United\n19/5/2024 15:00\n34343212 - 12.8817°4.00 FT 0 - 2\n(0 - 0)\nEPL\nBurnley\nNottingham Forest\n19/5/2024 15:00\n38332812 - 12.9819°2.90 FT 1 - 2\n(0 - 2)\n0.05\nEPL\nChelsea\nBournemouth\n19/5/2024 15:00\n49272412 - 12.7822°1.45 FT 2 - 1\n(1 - 0)\nEPL\nCrystal Palace\nAston Villa\n19/5/2024 15:00\n28314121 - 22.9122°3.80 FT 5 - 0\n(2 - 0)\n0.2\nEPL\nLiverpool\nWolverhampton\n19/5/2024 15:00\n63231413 - 04.1521°1.18 FT 2 - 0\n(2 - 0)\nEPL\nLuton Town\nFulham\n19/5/2024 15:00\n253936X2 - 23.4320°3.90 FT 2 - 4\n(1 - 2)\n0.18\nEPL\nManchester City\nWest Ham\n19/5/2024 15:00\n59261613 - 14.3422°1.10 FT 3 - 1\n(2 - 1)\nEPL\nSheffield United\nTottenham\n19/5/2024 15:00\n33175021 - 33.5321°1.36 FT 0 - 3\n(0 - 1)\nRound 37\nEPL\nFulham\nManchester City\n11/5/2024 11:30\n15196521 - 33.1921°1.25 FT 0 - 4\n(0 - 1)\nEPL\nBournemouth\nBrentford\n11/5/2024 14:00\n343729X1 - 12.3017°3.80 FT 1 - 2\n(0 - 0)\n0.15\nEPL\nEverton\nSheffield United\n11/5/2024 14:00\n55301513 - 02.6520°1.44 FT 1 - 0\n(1 - 0)\nEPL\nNewcastle United\nBrighton\n11/5/2024 14:00\n44322312 - 12.8221°1.50 FT 1 - 1\n(1 - 1)\nEPL\nTottenham\nBurnley\n11/5/2024 14:00\n61231613 - 13.5021°1.33 FT 2 - 1\n(1 - 1)\nEPL\nWest Ham\nLuton Town\n11/5/2024 14:00\n62251312 - 13.3821°1.75 FT 3 - 1\n(0 - 1)\n0.11\nEPL\nWolverhampton\nCrystal Palace\n11/5/2024 14:00\n30333720 - 22.2521°2.45 FT 1 - 3\n(0 - 2)\nEPL\nNottingham Forest\nChelsea\n11/5/2024 16:30\n21314821 - 33.3021°1.95 FT 2 - 3\n(1 - 1)\nEPL\nManchester United\nArsenal\n12/5/2024 15:30\n25235221 - 33.2723°1.40 FT 0 - 1\n(0 - 1)\nEPL\nAston Villa\nLiverpool\n13/5/2024 19:00\n283735X2 - 23.2415°4.20 FT 3 - 3\n(1 - 2)\n0.17\nEPL\nTottenham\nManchester City\n14/5/2024 19:00\n27235021 - 22.9515°1.33 FT 0 - 2\n(0 - 0)\nEPL\nBrighton\nChelsea\n15/5/2024 18:45\n273736X1 - 12.3016°4.00 FT 1 - 2\n(0 - 1)\n0.16\nEPL\nManchester United\nNewcastle United\n15/5/2024 19:00\n37323112 - 12.9216°2.63 FT 3 - 2\n(1 - 0)', \
            'Eu\nRomania\nNetherlands\n2/7/2024 16:00\n2',
            'Ca\nCosta Rica\nParaguay\n3/7/2024 1:00\nX']
    result_df = clean_data(sample_data)

    # Assert expected columns are present
    expected_columns = []

    assert list(result_df.columns) == expected_columns





# @patch('app.scraping.cm_scrapper')
# def test_completed_route(mock_cm_scrapper, client: FlaskClient):
#     mock_cm_scrapper.return_value = None  # Mock the scraper function
#     response = client.get('/matches/completed')

#     assert response.status_code == 200
#     assert response.get_json() == {'message': 'Scraping completed and data stored successfully'}

