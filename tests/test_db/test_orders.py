import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db.orders.models import Item, Order, OrderItem
from src.db.session import SessionLocal


@pytest.fixture
def db_session():
    """Crea una sessione di database per i test."""
    connection = SessionLocal().bind.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()



def test_create_item(db_session: Session):
    """Test per creare un oggetto Item."""
    item = Item(
        type="flower",
        name="Rose",
        size=10.5,
        price=5.99,
        available='{"stock": 100}',
    )
    db_session.add(item)
    db_session.commit()

    # Verifica che l'oggetto sia stato salvato
    saved_item = db_session.query(Item).filter_by(name="Rose").first()
    assert saved_item is not None
    assert saved_item.type == "flower"
    assert saved_item.size == 10.5


def test_unique_constraint_on_item(db_session: Session):
    """Test per verificare il vincolo di unicità su name e size."""
    item1 = Item(
        type="flower",
        name="Rose",
        size=10.5,
        price=5.99,
        available='{"stock": 100}',
    )
    item2 = Item(
        type="flower",
        name="Rose",
        size=10.5,
        price=6.99,
        available='{"stock": 50}',
    )
    db_session.add(item1)
    db_session.commit()

    # Aggiungere un duplicato dovrebbe sollevare un'eccezione
    db_session.add(item2)
    with pytest.raises(IntegrityError):
        db_session.commit()