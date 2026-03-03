FROM python:3.13-slim

# Empêche Python de générer des fichiers .pyc (plus propre)
ENV PYTHONDONTWRITEBYTECODE 1
# Permet aux logs de s'afficher en temps réel dans ton terminal
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout ton code source
COPY . .

# Expose le port par défaut du réseau sadcoin
EXPOSE 5000

# Lancement
CMD ["python", "main.py"]