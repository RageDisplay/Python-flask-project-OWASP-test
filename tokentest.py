from flask import Flask, render_template, session, request, redirect, url_for
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    # Генерация и сохранение CSRF-токена в сессии пользователя
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Проверка CSRF-токена из формы с сохраненным в сессии
    if 'csrf_token' in session and session['csrf_token'] == request.form.get('csrf_token'):
        # Действия, выполняемые при успешной проверке CSRF-токена
        # ...
        return "Всё хорошо"
    else:
        # Действия при недействительном CSRF-токене
        return "Ошибка"

if __name__ == '__main__':
    app.run()
    
"""<form action="/submit" method="post">
    <input type="hidden" name="csrf_token" value="{{ session['csrf_token'] }}">
    <button type="submit">Отправить</button>
</form>
"""