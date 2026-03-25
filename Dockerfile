FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

STOPSIGNAL SIGINT
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate --no-input && exec python manage.py runserver 0.0.0.0:8000"]
