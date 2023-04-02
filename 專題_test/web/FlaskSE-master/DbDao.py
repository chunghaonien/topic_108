from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DevDb.db'

# MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user_name:password@IP:3306/db_name"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://DevAuth:Dev127336@127.0.0.1:3306/DevDb"

app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class AppInfo(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String)
    version = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.Integer)
    remark = db.Column(db.String)

    def __init__(self, name, version, author, date, remark):
        self.name = name
        self.version = version
        self.author = author
        self.date = date
        self.remark = remark


@app.route('/')
def show_all():
    return render_template('data/show_all.html', appInfo=AppInfo.query.all())


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['version'] or not request.form['author']:
            flash('Please enter all the fields', 'error')
        else:
            info = AppInfo(request.form['name'], request.form['version'],
                           request.form['author'], request.form['date'], request.form['remark'])

            db.session.add(info)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('data/create.html')


@app.route('/delete/<app_id>', methods=['GET', 'POST'])
def modify(app_id):
    if request.method == 'GET':  # 這邊偷懶，用 Ajax 的 Delete 比較正確
        if not app_id:
            flash('Please enter the fields', 'error')
        else:
            appInfo = db.session.query(AppInfo).filter_by(id=app_id).first()
            print(appInfo)
            db.session.delete(appInfo)
            db.session.commit()
            flash('Record was successfully delete')
    return redirect(url_for('show_all'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
