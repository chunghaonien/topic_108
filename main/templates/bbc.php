<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
        <form method="POST" action="/bbc">
            <input type="checkbox" id="world" name="bbc" value="world"><b>國際</b>
            <input type="checkbox" id="china" name="bbc" value="china"><b>兩岸</b>
            <input type="checkbox" id="UA" name="bbc" value="UA"><b>英國</b>
            <input type="checkbox" id="technology" name="bbc" value="technology"><b>科技</b>
            <input type="checkbox" id="financial " name="bbc " value="financial "><b>財經</b>
            <br>
            起始頁數:<input type="text" id="start-page" name="start-page" size="2">
            結束頁數:<input type="text" id="end-page" name="end-page" size="2">
            <br>
            <input type="checkbox" id="save-data" name="save-data">
            <label for="save-data">儲存資料到 MySQL</label>
            <br>
            <button type='start'>開始</button>
            <form action="/table" method="POST">
                <input type="hidden" name="data" value="{{ data }}">
                <button type="submit">生成表格</button>
            </form>
        </form>
    </body>
</html>
