FROM python:3.12.6

RUN apt-get update && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

WORKDIR /app

CMD ["uvicorn src.main:app --host 0.0.0.0 --port 8000"]