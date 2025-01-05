# Use python base image compatible with Raspberry Pi (ARM architecture)
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY dashboard/ ./dashboard/
COPY data_collector/ ./data_collector/

# Create necessary directories
RUN mkdir -p data_collector/data

# Set environment variables
ENV FLASK_APP=dashboard/app.py
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"] 