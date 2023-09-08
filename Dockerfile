FROM python:3.8

ENV SECRET_KEY="KEYCHAIN"
ENV DATABASE_PASSWORD=$DATABASE_PASSWORD

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python", "app.py" ]

CMD waitress-serve --host 0.0.0.0 --port=8080  app:app
