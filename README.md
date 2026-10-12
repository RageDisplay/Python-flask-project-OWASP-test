Веб-форум на Python с использованием Flask
Данное приложение намеренно написано с уязвимостями под OWASP Top 10 и другими для тестирования и развития навыков

## Зависимости

- Flask
- Postgresql
- WTForms
- Flask-WTF

## Использование

1. Создать базу данных PostgreSQL и таблицы
2. Запустить app.py
3. В браузере перейти по адресу https://172.20.10.7:7000
4. Зарегистрироваться
5. Ввести логин и пароль
6. Ввести текст
7. Сохранить текст
8. Ввести поиск
9. Скачать текст
10. Скачать вручную

## Защита

Все запросы к базе данных и запросы к Flask-app проверяются с помощью CSRF-токена. Все запросы, которые не проходят проверку, будут отклонены с ошибкой 403.
Так же присутствует защита от SQL-инъекций и XSS-атак.

## Описание

### app.py

- app.py - основной файл Flask-app
- login_data - хранит логин и пароль пользователя
- csrf - CSRF-токен

### templates/

- login.html - страница входа
- input.html - страница ввода текста
- output.html - страница вывода текста
- search.html - страница поиска
- download.html - страница скачивания
- registration.html - страница регистрации

### static/ 

- styles/ - стили HTML-страниц
- images/ - изображения HTML-страниц

### TESTcreateusers.py

- TESTcreateusers.py - скрипт для создания пользователей и паролей

### TESTcreatetables.py

- TESTcreatetables.py - скрипт для создания таблиц в базе данных

## Ссылки

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/0.14.3/)
- [CSRF-токен](https://ru.wikipedia.org/wiki/Cross-site_request_forgery)

- docker build -t my_flask_app .
- docker run -p 7000:7000 --name my_container my_flask_app
- https://localhost:7000
