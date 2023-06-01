from flask import Flask, render_template, request
from mod.user import login, register

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == "POST":
        account = request.form.get('account')
        password = request.form.get('password')
        if login(account, password):
            return render_template('ok.html')
        else:
            return render_template('no.html')

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == "POST":
        account = request.form.get('account')
        password = request.form.get('password')
        username = request.form.get('username')
        if register(account, password, username):
            return render_template('ok.html')
        else:
            return render_template('no.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
