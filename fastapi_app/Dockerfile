FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose the API port
EXPOSE 8000

# Run Uvicorn server
CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8000"]