FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt update -y \
    apt install -y build-essential libpq-dev

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "run"]
