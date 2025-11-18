FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY "TOP 100 Songs of 2024 - Billboard Hot 100.csv" .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
