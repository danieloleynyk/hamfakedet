FROM python:3.9-slim-buster

ARG telegram_token
ENV TELEGRAM_TOKEN=$telegram_token

WORKDIR /bot

# installing dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python main.py
