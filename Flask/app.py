from flask import Flask, render_template, request
import mod.scraper
from mod.into_mysql import into_mysql
<<<<<<< HEAD
=======
import xlwt
import xlrd
from xlutils.copy import copy
>>>>>>> main

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    url = request.form['url-input']
    option = request.form.get('option', '')
    save_data = request.form.get('save-data')
    sql_date = ""

    if url == "":
        return render_template('index.html', date="請輸入網址")
    else:
        if option == 'html':
            date = mod.scraper.html(url)
        elif option == 'bs4':
            date = mod.scraper.bs4(url)
        elif option == '':
            date = '請選擇解析方式'

        if save_data:
            sql_date = into_mysql(url, date)

        return render_template('index.html', date=date, sql_date=sql_date)

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
=======
def write_excel(data):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    for i in range(len(data)):
        for j in range(len(data[i])):
            sheet.write(i, j, data[i][j])
    wbk.save('data.xls')

def read_excel():
    data = []
    wb = xlrd.open_workbook('data.xls')
    sheet = wb.sheet_by_index(0)
    for i in range(sheet.nrows):
        data.append(sheet.row_values(i))
    return data

def add_excel(data):
    rb = xlrd.open_workbook('data.xls')
    wb = copy(rb)
    ws = wb.get_sheet(0)
    for i in range(len(data)):
        for j in range(len(data[i])):
            ws.write(i, j, data[i][j])
    wb.save('data.xls')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)



>>>>>>> main
