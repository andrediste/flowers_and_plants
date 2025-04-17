import streamlit as st
from sqlalchemy.orm import Session

from db.orders.models import Item
from db.session import get_session


def show_item_form(db: Session, item: Item = None):
    st.subheader("Add / Edit Item")
    name = st.text_input("Name", value=item.name if item else "")
    type_ = st.text_input("Type", value=item.type if item else "")
    size = st.number_input("Size", value=item.size if item and item.size else 0.0)
    price = st.number_input("Price", value=item.price if item and item.price else 0.0)
    available = st.text_input("Available (comma separated)", value=item.available if item else "")

    if st.button("Save", key="save_item"):
        if item:
            item.name = name
            item.type = type_
            item.size = size
            item.price = price
            item.available = available
        else:
            new_item = Item(name=name, type=type_, size=size, price=price, available=available)
            db.add(new_item)
        db.commit()
        st.success("Item saved!")
        st.rerun()


def manage_inventory():
    st.title("Gestione Inventario")

    db: Session = get_session()

    items = db.query(Item).all()
    st.subheader("Inventario")

    for item in items:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"**{item.name}** ({item.type}) - {item.size} - {item.price} ")
            st.caption(f"Available: {item.available}")
        with col2:
            if st.button("Edit", key=f"edit_{item.id}"):
                show_item_form(db, item)
        with col3:
            if st.button("Delete", key=f"delete_{item.id}"):
                db.delete(item)
                db.commit()
                st.warning("Deleted")
                st.rerun()

    st.markdown("---")
    if st.checkbox("+ Aggiungi nuovo articolo"):
        show_item_form(db)


# entry point
manage_inventory()
