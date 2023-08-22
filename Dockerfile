# Usa un'immagine di Python come base
FROM python:3.9

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia i file requirements.txt e app.py nella directory di lavoro del container
COPY requirements.txt .
#COPY flask_app.py .
COPY . .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta 5000 per l'accesso all'applicazione
EXPOSE 5000

# Avvia l'applicazione quando il container viene eseguito
CMD ["python", "flask_app.py"]
