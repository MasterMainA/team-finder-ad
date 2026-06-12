FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y fonts-dejavu-core

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"