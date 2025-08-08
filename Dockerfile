FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev netcat-traditional curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["bash", "./entrypoint.sh"]