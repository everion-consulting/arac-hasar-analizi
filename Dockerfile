FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Sistem bağımlılıkları (psycopg2 için)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyaları
COPY . .

# Static dosyaları topla
RUN DJANGO_SETTINGS_MODULE=django_arac_hasar_backend.settings \
    python django_arac_hasar_backend/manage.py collectstatic --noinput

# Django projesi alt klasörde duruyor: /app/django_arac_hasar_backend
# manage.py'nin yanına geçiyoruz ki `django_arac_hasar_backend.wsgi` modülü bulunabilsin.
WORKDIR /app/django_arac_hasar_backend

# Django ayar modu
ENV DJANGO_SETTINGS_MODULE=django_arac_hasar_backend.settings

# Varsayılan komut (production için gunicorn ile Django)
CMD ["gunicorn", "django_arac_hasar_backend.wsgi:application", "--bind", "0.0.0.0:8000"]

