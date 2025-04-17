# Flower Shop Manager

Gestione automatica di ordini per un negozio di fiori, integrata con OCR, Streamlit, Google Drive, Telegram.

## Requisiti
- Python 3.10+
- Streamlit
- SQLAlchemy
- Google API Client
- Telegram Bot API

## Setup rapido
1. Crea un file `.env` con token telegram, ID chat, e credenziali Google Drive.
2. Esegui l'app Streamlit: `streamlit run src/app.py`.
3. Imposta l'accesso al file su Google Drive.

## Telegram
- Crea un bot su BotFather.
- Salva il token nel `.env`.
- Ottieni il tuo ID chat (puoi usare @get_id_bot su Telegram).

## Google Drive
- Crea un progetto in Google Cloud Console.
- Abilita l'API di Drive e scarica `credentials.json`.

## Database
Due opzioni disponibili:
- Locale (`app/data/flower_shop_test.sqlite`)
- Produzione su Google Drive (`/mount/drive/flower_shop_prod.sqlite`)


docker run --rm -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=postgres postgres:15
docker exec postgres psql -h localhost -U postgres --command "create database flower_and_plants;"
alembic upgrade head

docker run --rm -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=postgres postgres:15

docker stop postgres # only works if the container was started with `docker run --rm`

docker exec postgres psql -h localhost -U postgres --command "drop database flower_and_plants;" 