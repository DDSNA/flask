FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG SECRETS_FILE=secrets.txt
RUN while IFS='=' read -r key value; do \
    export "$key"="$value"; \
done < "$SECRETS_FILE"

EXPOSE 8080

CMD [ "python", "app.py" ]

CMD waitress-serve --host 0.0.0.0 --port=8080  app:app
