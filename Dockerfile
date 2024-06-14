# docker compose up --build -d
# To run the container in interactive mode
# docker compose run app bash

FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2 \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libgdk-pixbuf2.0-0 \
    libgdk-pixbuf2.0-dev \
    libpango-1.0-0 \
    libpango1.0-dev \
    libcairo2 \
    libcairo2-dev \
    pango1.0-tools \
    libgirepository1.0-dev \
    gir1.2-pango-1.0 \
    gobject-introspection \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run the application with Gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "cabmaster.wsgi:application"]
