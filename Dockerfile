FROM python:3.11-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y ffmpeg libpq-dev gcc

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]