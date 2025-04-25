FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y dos2unix && rm -rf /var/lib/apt/lists/*

COPY . .

RUN dos2unix /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "-u", "app.py"]

EXPOSE 8000