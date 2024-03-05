Веб-форум на Python с использованием Flask

## Зависимости

- Flask
- SQLite
- WTForms
- Flask-WTF

## Использование

1. Создать базу данных SQLite
2. Запустить app.py
3. В браузере перейти по адресу http://localhost:7000
4. Ввести логин и пароль
5. Ввести текст
6. Сохранить текст
7. Ввести поиск
8. Скачать текст
9. Скачать вручную 

## Защита

Все запросы к базе данных и запросы к Flask-app проверяются с помощью CSRF-токена. Все запросы, которые не проходят проверку, будут отклонены с ошибкой 403.
Так же присутствует защита от SQL-инъекций и XSS-атак.

## Описание

### app.py

- app.py - основной файл Flask-app
- db_path - путь к базе данных
- login_data - хранит логин и пароль пользователя
- csrf - CSRF-токен

### templates/

- login.html - страница входа
- input.html - страница ввода текста
- output.html - страница вывода текста
- search.html - страница поиска
- download.html - страница скачивания

### static/ 

- styles/ - стили HTML-страниц
- images/ - изображения HTML-страниц

### TESTcreateusers.py

- TESTcreateusers.py - скрипт для создания пользователей и паролей

### TESTcreatetables.py

- TESTcreatetables.py - скрипт для создания таблиц в базе данных

## Ссылки

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [SQLite](https://www.sqlite.org/index.html)
- [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/0.14.3/)
- [CSRF-токен](https://ru.wikipedia.org/wiki/Cross-site_request_forgery)
