<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
        <form method="POST" action="/bahamut">

            <br>
            起始頁數:<input type="text" id="start-page" name="start-page" size="2">
            結束頁數:<input type="text" id="end-page" name="end-page" size="2">
            <br>
            <input type="checkbox" id="save-data" name="save-data">
            <label for="save-data">儲存資料到 MySQL</label>
            <br>
            <button>開始</button>
        </form>
        <form action="/table" method="POST">
            <input type="hidden" name="data" value="{{ data }}">
            <button type="submit">生成表格</button>
        </form>
        
    </body>
</html>
