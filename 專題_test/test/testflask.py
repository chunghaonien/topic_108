from flask import Flask, request, render_template
import urllib.request as req
import urllib.error as err

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url-input']
        try:
            response = req.urlopen(url)
            content = response.read().decode('UTF-8')
            return render_template('index.html', content=content, url_input=url)
        except err.URLError as e:
            return render_template('index.html', error=str(e))
    else:
        return render_template('index.html')

@app.route('/get_code', methods=['POST'])
def get_code():
    url = request.form['url']
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
    }
    request = req.Request(url = url, headers = headers)
    try:
        response = req.urlopen(request)
        content = response.read().decode('utf-8')
        return content
    except err.URLError as e:
        return '發生錯誤：{}'.format(e)

if __name__ == '__main__':
    app.run(debug=True)
