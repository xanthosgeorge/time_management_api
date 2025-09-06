
# Χρησιμοποιούμε Python 3.12 slim image
FROM python:3.12-slim

# Δημιουργία φακέλου app
WORKDIR /app

# Αντιγραφή απαιτήσεων (requirements.txt) και εγκατάσταση
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Αντιγραφή του κώδικα του API
COPY . .

# Default port
EXPOSE 5000

# Εκκίνηση εφαρμογής (Flask παράδειγμα)
# Εκκίνηση με gunicorn (παράδειγμα: app.py έχει Flask app με όνομα "app")
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     PIP_NO_CACHE_DIR=1 \
#     JENKINS_HOME=/var/jenkins_home

# WORKDIR /app

# # Install build deps for bcrypt and Jenkins dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential libffi-dev python3-dev \
#     openjdk-17-jdk curl gnupg2 \
#     && rm -rf /var/lib/apt/lists/*

# # Install Jenkins (LTS version)
# RUN curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | gpg --dearmor -o /usr/share/keyrings/jenkins-keyring.gpg \
#     && echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.gpg] https://pkg.jenkins.io/debian-stable binary/" > /etc/apt/sources.list.d/jenkins.list \
#     && apt-get update && apt-get install -y jenkins \
#     && rm -rf /var/lib/apt/lists/*

# # Python dependencies
# COPY requirements.txt ./
# RUN pip install --upgrade pip setuptools wheel
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy app code
# COPY . .

# # Expose both Flask and Jenkins ports
# EXPOSE 5000 8080

# # Start both services using supervisord
# RUN pip install supervisor
# COPY supervisord.conf /etc/supervisord.conf

# CMD ["supervisord", "-c", "/etc/supervisord.conf"]
