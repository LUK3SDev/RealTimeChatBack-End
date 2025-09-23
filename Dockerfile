# Usa un'immagine base di Python
FROM python:3.10-slim

# Imposta le variabili d'ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia il file dei requisiti e installa le dipendenze
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice della tua applicazione
COPY . /app/

# Espone la porta su cui l'applicazione sarà in ascolto
EXPOSE 8000