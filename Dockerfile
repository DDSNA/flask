FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY $SECRET_KEY
ENV FRONTEND_KEY $FRONTEND_KEY
ENV UP_KEY $UP_KEY
ENV FRONTEND_DB $FRONTEND_DB
ENV UP_DB $UP_DB

EXPOSE 8080

CMD [ "python", "app.py" ]

CMD waitress-serve --host 0.0.0.0 --port=8080  app:app
