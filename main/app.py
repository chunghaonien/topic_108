from flask import Flask, render_template, request
import mod.scraper
from mod.into_mysql import into_mysql
import mod.execl
import web.bahamut.bahamut_1


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    url = request.form['url-list']
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
        if url == "bahamut":
            for i in range(start_page, end_page+1):
                base_url = 'https://forum.gamer.com.tw/B.php?page='+ str(i) +'&bsn=36730'         
                data = web.bahamut.bahamut_1.start_bahamut(base_url)
    
    if save_data:
        sql_data = into_mysql(url, data)

    return render_template('index.html', data=data, sql_data=sql_data)

#在html上按下按鈕，取得執行完成的內容生成表格
@app.route('/table', methods=['POST'])
def table():
    data = request.form['data']
    #把data切成二維陣列
    done_data = []
    count_a = 0
    count_b = 1
    for i in data:
        
    #生成表格
    table_html = '<table><tr><td>標題</td><td>內容</td></tr>'
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
