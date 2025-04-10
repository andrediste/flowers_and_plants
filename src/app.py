import streamlit as st
from datetime import date
from infrastructure.db.database import init_db, insert_order

# Inizializzazione DB
init_db()

st.title("📦 Nuovo ordine")

st.subheader("Informazioni ordine")

shop = st.text_input("Negozio", value="Recco")
data_ordine = st.date_input("Data ordine", value=date.today())
note = st.text_area("Note o metadati (opzionale)")

st.markdown("---")
st.subheader("Articoli dell'ordine")

# Per semplicità, supportiamo fino a 5 articoli per ordine
articoli = []
for i in range(1, 6):
    with st.expander(f"Articolo #{i}"):
        nome = st.text_input(f"Nome pianta #{i}", key=f"item_{i}")
        size = st.number_input(f"Taglia (cm) #{i}", min_value=0.0, step=0.5, key=f"size_{i}")
        quantity = st.number_input(f"Quantità #{i}", min_value=0, step=1, key=f"quantity_{i}")
        meta = st.text_input(f"Metadata (opzionale) #{i}", key=f"meta_{i}")
        if nome and quantity > 0:
            articoli.append({
                "item": nome,
                "size": size,
                "quantity": quantity,
                "metadata": meta if meta else None
            })

if st.button("📤 Invia ordine"):
    if not articoli:
        st.warning("Inserisci almeno un articolo per inviare l’ordine.")
    else:
        order_data = {
            "shop": shop,
            "date": data_ordine.isoformat(),
            "metadata": note
        }
        insert_order(order_data, articoli)
        st.success(f"Ordine inviato con successo! ({len(articoli)} articoli)")
        st.balloons()
