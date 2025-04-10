from infrastructure.db.database import init_db, insert_order, get_orders_by_shop_and_date
from datetime import date

init_db()

order_data = {
    "shop": "Recco",
    "date": date.today().isoformat()
}

items = [
    {"item": "Ortensia", "size": 30.0, "quantity": 3},
    {"item": "Lavanda", "size": 15.0, "quantity": 5},
    {"item": "Girasole", "size": 40.0, "quantity": 2}
]

insert_order(order_data, items)

result = get_orders_by_shop_and_date("Recco", date.today().isoformat())
for row in result:
    print(row)