FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We don't copy the data folder here because it is mounted via docker-compose
COPY . .

CMD ["python", "-u", "main.py"] 
# Note: -u forces unbuffered output so print() statements show up immediately in Docker logs