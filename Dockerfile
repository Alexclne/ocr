FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Set working directory
WORKDIR /app

# Copy your code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir python-doctr[torch] opencv-python-headless

# Run the script
CMD ["python", "main.py"]
