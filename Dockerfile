FROM python:3.11-alpine

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev postgresql-client

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY /static/styles/. /app/static/styles

COPY /templates/. /app/templates

COPY . /app

USER postgres

RUN /etc/init.d/postgresql start &&\ psql --command "CREATE USER postgres WITH PASSWORD 'pass';" &&\ createdb -O postgres auth

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/13/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/13/main/postgresql.conf

USER root

CMD service postgresql start && python app.py
