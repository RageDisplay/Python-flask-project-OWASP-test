# Устанавливаем базовый образ
FROM ubuntu:22.04

# Устанавливаем переменную окружения для noninteractive режима
ENV DEBIAN_FRONTEND=noninteractive

# Обновляем пакеты и устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y sudo python3 python3-pip postgresql postgresql-contrib postgresql-server-dev-all gcc musl-dev python3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN usermod -aG sudo postgres
# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем статические файлы и шаблоны
COPY /static/styles/. /app/static/styles
COPY /templates/. /app/templates
COPY . /app

# Переключаемся на пользователя postgres
USER postgres

# Меняем метод аутентификации в конфигурационном файле PostgreSQL
RUN sed -i 's/md5/trust/g' /etc/postgresql/14/main/pg_hba.conf

# Запускаем PostgreSQL, меняем пароль пользователя postgres, создаем базу данных и останавливаем сервис PostgreSQL
RUN service postgresql start && psql --command "ALTER USER postgres WITH PASSWORD 'pass';" && sudo -u postgres createdb auth && service postgresql stop

# Добавляем правило доступа к PostgreSQL в pg_hba.conf
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/14/main/pg_hba.conf

# Включаем прослушивание всех адресов в файле postgresql.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/14/main/postgresql.conf

# Переключаемся обратно на пользователя root
USER root

# Запускаем сервис PostgreSQL и запускаем приложение
CMD service postgresql start && python3 TESTcreatetables.py && python3 TESTcreateusers.py && python3 app.py
# 