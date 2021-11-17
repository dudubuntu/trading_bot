FROM python:3.7-slim

WORKDIR /var/www/trading_bot/

COPY requirements.txt /var/www/trading_bot/
RUN pip install -r /var/www/trading_bot/requirements.txt
COPY . /var/www/trading_bot/