# Usa un'immagine base di Python
FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Aggiorna pip e installa Poetry
RUN pip install --no-cache-dir --upgrade pip \
    && pip install poetry
    
# Copia solo i file necessari per installare le dipendenze
COPY pyproject.toml poetry.lock ./

# Installa le dipendenze del progetto senza creare un ambiente virtuale
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copia il resto del codice sorgente
COPY . .

# Espone la porta usata da Streamlit
EXPOSE 8501

# Comando per avviare Streamlit
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.enableCORS=false"]