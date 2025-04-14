import pandas as pd

from db.orders.models import Item
from db.session import get_session


def import_items_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    session = get_session()
    for _, row in df.iterrows():
        item = Item(
            name=row["name"],
            type=row["type"],
            size=row["size"],
            price=row["price"],
            available_tags=row.get("available_tags", ""),
        )
        session.add(item)
    session.commit()
