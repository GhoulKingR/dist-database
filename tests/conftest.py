from agents import create_app
import pytest
import sqlite3

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    yield app

@pytest.fixture
def agentdb():
    try:
        conn = sqlite3.connect("databases/grp9agents.db")
        yield conn

    except sqlite3.Error as err:
        print("An SQL error occured:", err)
        return {}, 500  # internal server error
    
    finally:
        if conn:
            conn.close()
            print("Sqlite3 connection closed")

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()