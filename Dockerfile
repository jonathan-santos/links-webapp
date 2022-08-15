FROM python:3.10-slim-bullseye

RUN apt update -y \
    && apt install -y build-essential libpq-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "app:init_app()" ,"--preload"]
