from datetime import datetime

import streamlit as st
from sqlalchemy.orm import Session

from db.orders.models import Item, Order, OrderItem
from db.session import get_session


def ordini_page():
    st.title("Gestione Ordini")

    db: Session = get_session()

    tabs = st.tabs(["Nuovo ordine", "Ordini esistenti", "Gestione ordine"])

    with tabs[0]:
        st.header("Crea un nuovo ordine")
        shop = st.text_input("Negozio")
        note = st.text_area("Note aggiuntive")

        items = db.query(Item).all()
        order_items = []
        st.subheader("Seleziona articoli")
        for item in items:
            col1, col2 = st.columns([4, 1])
            with col1:
                quantity = st.number_input(
                    f"{item.name} {item.size} ({item.type})",
                    0,
                    100,
                    step=1,
                    key=f"qty_{item.id}",
                )
            with col2:
                if quantity > 0:
                    order_items.append((item, quantity))

        if st.button("Invia ordine"):
            new_order = Order(
                shop=shop,
                date=datetime.now(),
                note=note,
            )
            db.add(new_order)
            db.commit()
            db.refresh(new_order)

            for item, qty in order_items:
                oi = OrderItem(
                    order_id=new_order.id,
                    item_id=item.id,
                    quantity=qty,
                )
                db.add(oi)
            db.commit()
            st.success("Ordine creato con successo!")

    with tabs[1]:
        st.header("Lista ordini")
        orders = db.query(Order).all()
        for o in orders:
            with st.expander(f"Ordine #{o.id} - {o.shop} - {o.date.strftime('%d/%m/%Y')}"):
                st.text(o.note)
                st.text(f"Gestito: {'✔️' if o.handled else '❌'}")
                for item in o.items:
                    st.text(
                        f"{item.item.name} - {item.item.size} x{item.quantity}  - {item.item.price}€"
                    )

    with tabs[2]:
        st.header("Preparazione ordini")
        non_gestiti = db.query(Order).filter_by(handled=False).all()
        if not non_gestiti:
            st.info("Nessun ordine da gestire")
        else:
            selezionato = st.selectbox(
                "Scegli un ordine da gestire",
                non_gestiti,
                format_func=lambda x: f"#{x.id} - {x.shop} - {x.date}",
            )
            if selezionato:
                for item in selezionato.items:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        item.checked = st.checkbox(
                            f"{item.item.name} - {item.item.size}",
                            key=f"check_{item.id}",
                        )
                    with col2:
                        item.prepared_quantity = st.number_input(
                            "Quantità preparata",
                            min_value=0,
                            value=item.quantity,
                            key=f"realqty_{item.id}",
                        )

                if st.button("Conferma ordine preparato"):
                    selezionato.handled = True
                    db.commit()
                    st.success("Ordine segnato come gestito")
