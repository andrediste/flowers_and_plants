import pytest
from sqlalchemy.exc import OperationalError

from src.db.session import engine


def test_database_connection():
    """Test per verificare la connessione al database."""
    try:
        connection = engine.connect()
        connection.close()
    except OperationalError:
        pytest.fail("Impossibile connettersi al database")