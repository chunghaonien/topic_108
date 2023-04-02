from flask import Flask, render_template, request
from mod.scraper import scrape_website
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from mod.into_mysql import into_mysql


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST' and 'start' in request.form:
        url = request.form['url-input']
        if url == "":
            return render_template('index.html', data="請輸入網址")
        else:
            date = scrape_website(url)
            return render_template('index.html', date=date)
    else:
        return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def into_botton():
    if request.method == 'POST' and 'go' in request.form:
        if 'url-input' in request.form and 'date' in request.form:
            url = request.form['url-input']
            date = request.form['date']

            date1 = into_mysql(url, date)

            return render_template('index.html', date='date1')
        else:
            return render_template('index.html', date='請輸入網址和程式碼')
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
