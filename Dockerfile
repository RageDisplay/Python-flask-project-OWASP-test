<<<<<<< HEAD
FROM python:3.11-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY /static/styles/. /app/static/styles

COPY /templates/. /app/templates

COPY . /app

CMD ["python", "app.py"]

=======
FROM python:3.11-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY /static/styles/. /app/static/styles

COPY /templates/. /app/templates

COPY . /app

CMD ["python", "app.py"]

>>>>>>> f3d80e8c21dd62c97cc0cdf113c63483833025c1
