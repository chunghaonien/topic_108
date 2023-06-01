from flask import Flask, render_template, request, jsonify
from mod.user import login, register, get_user_data

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

user_logged_in = False
global login_account
global login_password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login_route():
    account = request.form.get('account')
    password = request.form.get('password')
    if login(account, password):
        login_account = account
        login_password = password
        user = get_user_data(login_account, login_password)

        return render_template('index.html', user_logged_in=True, username=user[0]['username'], user_data=jsonify(user))
    else:
        return render_template('no.html')


@app.route('/register', methods=['POST', 'GET'])
def register_route():

    account = request.form['account']
    password = request.form['password']
    username = request.form['username']

    if register(account, password, username):
        return render_template('ok.html')
    else:
        return render_template('no.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
