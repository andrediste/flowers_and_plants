import streamlit as st

from services.csv_import import import_items_from_csv

st.title("Importa Articoli da CSV")

uploaded_file = st.file_uploader("Carica file CSV", type=["csv"])
if uploaded_file:
    import_items_from_csv(uploaded_file)
    st.success("Articoli importati con successo!")
