FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8083

CMD ["python", "main.py"]
