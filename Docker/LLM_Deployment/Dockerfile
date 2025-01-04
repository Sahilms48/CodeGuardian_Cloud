FROM python:3.9-slim

# Install necessary tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Install llama-cpp-python for model inference and Flask, GCS libraries
RUN pip install flask google-cloud-storage llama-cpp-python

# Copy the service account key for GCP authentication
COPY service_account.json /app/service_account.json

# Copy the Flask application code
COPY app.py /app/app.py

# Set the working directory
WORKDIR /app

# Expose the port Flask will run on
EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]
