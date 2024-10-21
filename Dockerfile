FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
         build-essential \
         gcc \
         libpq-dev \
         && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .env ./
COPY *.py ./
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

# At runtime, use the .env file
CMD ["python", "main.py"]