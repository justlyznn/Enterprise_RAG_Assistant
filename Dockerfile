FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port for Hugging Face Spaces (default 7860)
EXPOSE 7860

# Run FastAPI, which now also mounts the Chainlit UI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
