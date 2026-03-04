FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie TOUT le code d'abord
COPY . .

# On teste ensuite
RUN pytest tests/

EXPOSE 5000
CMD ["python", "main.py"]