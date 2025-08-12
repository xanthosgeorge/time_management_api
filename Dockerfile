FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# build deps για bcrypt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
# Αν το app.py έχει "app = Flask(__name__)"
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]



# FROM python:3-alpine3.12
# # Set the working directory
# WORKDIR /app
# # Copy the requirements file into the container
# COPY . /app/
# RUN pip install -r requirements.txt

# # Expose the port the app runs on
# EXPOSE 5000
# CMD  python app.py