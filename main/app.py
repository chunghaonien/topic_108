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
    date = ""
    sql_date = ""
    if start_page == "" or end_page == "":
        date = '請輸入頁數'
    else:
        start_page = int(start_page)
        end_page = int(end_page)
        if url == "bahamut":
            for i in range(start_page, end_page+1):
                base_url = 'https://forum.gamer.com.tw/B.php?page='+ str(i) +'&bsn=36730'         
                date = web.bahamut.bahamut_1.start_bahamut(base_url)
    
    if save_data:
        sql_date = into_mysql(url, date)

    return render_template('index.html', date=date, sql_date=sql_date)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
