FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .env ./
COPY *.py ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# At runtime, use the .env file
CMD ["python", "main.py"]