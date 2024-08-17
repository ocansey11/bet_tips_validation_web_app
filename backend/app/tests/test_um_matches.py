import pytest #type:ignore
from app import create_app
from app.config import TestingConfig
from app.utils import db, migrate
from flask_migrate import upgrade #type:ignore


@pytest.fixture()
def app():
    test_app = create_app(TestingConfig)
    app.config.update({
        "TESTING": True,
    })

    db.init_app(app)
    migrate.init_app(test_app, db)

    with test_app.app_context():
        upgrade()  # Apply migrations to the test database

    yield test_app

    # Cleanup
    db.drop_all()  # Optionally drop all tables to reset the database


def test_request_example(client):
    response = client.get("/admin")
    assert b"<h1>Admin Page</h1>" in response.data