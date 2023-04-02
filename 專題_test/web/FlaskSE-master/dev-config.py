import flask

app = flask.Flask(__name__)


@app.route("/")
@app.route("/hello")
def hello():
    return "Hello, World ~ !!! Text Text Text ~ !!!"


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
