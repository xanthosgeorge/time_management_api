FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# μόνο τα requirements για καλύτερο caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# τώρα όλος ο κώδικας (αφού δεν έχεις φάκελο app/)
COPY . .

EXPOSE 5000
# το Flask object είναι στο app.py ως "app"
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