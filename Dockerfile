# ----------------------------------------------------------------------
# Phase 1 Dockerfile — builds the Book Shop Django backend image from source.
# Phase 2 (dev/test branches) replaces this file with Dockerfile.artifact
# which builds the image FROM a saved artifact instead of from source.
# ----------------------------------------------------------------------
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System deps needed for psycopg2-binary at runtime + build hygiene
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better Docker layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy Django project source (the upstream repo keeps the project under book-shop/)
COPY book-shop/ /app/

# Entrypoint waits for Postgres, runs migrate + collectstatic, then exec's gunicorn
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "book_shop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
