import mysql.connector
from flask import Flask, request, render_template, redirect, session

app = Flask(__name__)
app.secret_key = '1234567890'  # Секретный ключ для сессий Flask

# Параметры подключения к базе данных
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database_name'
}

# Счетчик неправильных попыток
MAX_ATTEMPTS = 10


def check_credentials(username, password):
    """
    Функция для проверки учетных данных пользователя в базе данных.
    Возвращает True, если учетные данные совпадают, и False в противном случае.
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)

        result = cursor.fetchone()[0]
        return result > 0

    except mysql.connector.Error as error:
        print('Ошибка при выполнении запроса: ', error)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка учетных данных
        if check_credentials(username, password):
            # Учетные данные правильные, устанавливаем сессию
            session['logged_in'] = True
            session['attempts'] = 0
            return redirect('/result')
        else:
            # Учетные данные неправильные, увеличиваем счетчик попыток
            session['attempts'] = session.get('attempts', 0) + 1
            if session['attempts'] >= MAX_ATTEMPTS:
                # Блокировка после превышения лимита попыток
                return "Превышено количество попыток. Блокировка отправки."
            else:
                return "Неправильные учетные данные. Пожалуйста, повторите попытку."

    return render_template('login.html')


@app.route('/result')
def result():
    if not session.get('logged_in'):
        # Если пользователь не аутентифицирован, перенаправляем на страницу входа
        return redirect('/')
    else:
        return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
