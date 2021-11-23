FROM python:3

WORKDIR /var/www/app/

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "/var/www/app/entrypoint.sh" ]