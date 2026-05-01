FROM python:3.11-slim

WORKDIR /app

COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=catalogue_livre.settings

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]