from flask import Flask, render_template, request
import mod.scraper
from mod.into_mysql import into_mysql
import mod.execl
import web.bahamut.bahamut_1
from web.BBC.BBC_list  import get_options, start_bbc


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('index.php')

@app.route('/web/<page>')
def web(page):
    if page == 'bahamut':
        return render_template('bahamut.php')
    elif page == 'ptt':
        return render_template('ptt.php')
    elif page == 'dcard':
        return render_template('dcard.php')
    elif page == 'yahoo':
        return render_template('yahoo.php')
    elif page == 'mobile01':
        return render_template('mobile01.php')
    elif page == 'bbc':
        return render_template('bbc.php')
    else:
        return 'Page not found'

@app.route('/bahamut', methods=['POST'])
def bahamut():
    save_data = request.form.get('save-data')
    start_page = request.form.get('start-page')
    end_page = request.form.get('end-page')
    data = ""
    sql_data = ""
    if start_page == "" or end_page == "":
        data = '請輸入頁數'
    else:
        start_page = int(start_page)
        end_page = int(end_page)

        if save_data:
            sql_data = into_mysql(url, data)
            if sql_data:
                return render_template('success.html')
            else:
                return render_template('error.html')

    return render_template('index.php', data=data, sql_data=sql_data)

@app.route('/bbc', methods=['POST'])
def bbc():
    options_list = request.form.getlist('bbc')
    save_data = request.form.get('save-data')
    start_page = request.form.get('start-page')
    end_page = request.form.get('end-page')
    data = ""
    sql_data = ""
    if start_page == "" or end_page == "":
        data = '請輸入頁數'
    else:
        start_page = int(start_page)
        end_page = int(end_page)
        if options_list == []:
            data = '請選擇分類'
        else:
            url_list = get_options(options_list)
            for url in url_list:
                for i in range(start_page, end_page + 1):
                    url = url + 'page=' + str(i)
                    for d in start_bbc(url):
                        data += d
                        data += '<br>'
            

    return render_template('index.php', data=data)

@app.route('/table', methods=['POST'])
def table():
    data = request.form['data']
    done_data = []
    count_a = 0
    count_b = 1
    for i in data:
        table_html = ''
        for row in data:
            table_html += '<tr>'
            table_html += '<td>' + row[0] + '</td>'
            table_html += '<td>' + row[1] + '</td>'
            table_html += '</tr>'
        table_html += '</table>'
    # 回傳表格
    return table_html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
