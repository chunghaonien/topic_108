from flask import Flask, render_template, request, jsonify, url_for, redirect, session
from mod.user import login, register, get_user_data

app = Flask(__name__)

user_logged_in = False
login_account = None
login_password = None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page_switch', methods=['POST', 'GET'])
def page_switch_route():
    page = request.form['page']
    if page == 'settings':
        return redirect(url_for('settings'))
    elif page == 'index':
        return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    return render_template('user-set.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    global user_logged_in
    global login_account
    global login_password

    user_logged_in = False
    login_account = None
    login_password = None

    return render_template('index.html')

@app.route('/get_user_data', methods=['GET'])
def get_user_data_route():
    user_data = get_user_data(login_account, login_password)
    user_data = user_data[0] if user_data else []

    return jsonify(user_data)


@app.route('/login', methods=['POST', 'GET'])
def login_route():
    global login_account
    global login_password

    account = request.form['account']
    password = request.form['password']
    if login(account, password):
        login_account = account
        login_password = password
        user_data_list = get_user_data(login_account, login_password)

        if user_data_list:
            user_data = user_data_list[0]
            return render_template('index.html', user_logged_in=True, username=user_data['username'])
        else:
            return render_template('index.html', user_logged_in=True, username=None)
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
