from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    return redirect(f'/result?name={name}&email={email}&message={message}')

@app.route('/result')
def show_result():
    name = request.args.get('name')
    email = request.args.get('email')
    message = request.args.get('message')
    return render_template('result.html', name=name, email=email, message=message)

if __name__ == '__main__':
    app.run(debug=True)
