<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
        <form method="POST" action="/start">
            <input type="checkbox" id="cosmetic" name="dcard" value="cosmetic"><b>美妝</b>
            <input type="checkbox" id="outfit" name="dcard" value="outfit"><b>穿搭</b>
            <input type="checkbox" id="shopping" name="dcard" value="shopping"><b>購物</b>
            <input type="checkbox" id="emotion" name="dcard" value="emotion"><b>感情</b>
            <input type="checkbox" id="constellation" name="dcard" value="constellation"><b>星座</b>
            <input type="checkbox" id="rainbow" name="dcard" value="rainbow "><b>彩虹</b>
            <input type="checkbox" id="chat " name="dcard" value="chat "><b>閒聊</b>
            <input type="checkbox" id="current events" name="dcard" value="current events"><b>時事</b>
            <input type="checkbox" id="music " name="dcard" value="music"><b>音樂</b>
            <input type="checkbox" id="movie" name="dcard" value="movie"><b>電影</b><br>
            <input type="checkbox" id="star" name="dcard" value="star"><b>明星</b>
            <input type="checkbox" id="art" name="dcard" value="art"><b>藝術</b>
            <input type="checkbox" id="life" name="dcard" value="life"><b>生活</b>
            <input type="checkbox" id="boutique" name="dcard" value="boutique"><b>精品</b>
            <input type="checkbox" id="pet" name="dcard" value="pet"><b>寵物</b>
            <input type="checkbox" id="food" name="dcard" value="food"><b>美食</b>
            <input type="checkbox" id="living abroad" name="dcard" value="living abroad"><b>海外生活</b>
            <input type="checkbox" id="travel" name="dcard" value="travel"><b>旅遊</b>
            <input type="checkbox" id="japan" name="dcard" value="japan"><b>日本</b>
            <input type="checkbox" id="korea" name="dcard" value="korea"><b>韓國</b><br>
            <input type="checkbox" id="game" name="dcard" value="game"><b>遊戲</b>
            <input type="checkbox" id="entertainment" name="dcard" value="entertainment"><b>休閒娛樂</b>
            <input type="checkbox" id="anime" name="dcard" value="anime"><b>動漫</b>
            <input type="checkbox" id="3C" name="dcard" value="3C"><b>3C</b>
            <input type="checkbox" id="science" name="dcard" value="science"><b>科學</b>
            <input type="checkbox" id="finance" name="dcard" value="finance"><b>金融</b>
            <input type="checkbox" id="transportation" name="dcard" value="transportation"><b>交通</b>
            <input type="checkbox" id="physical education" name="dcard" value="physical education"><b>體育</b>
            <input type="checkbox" id="medical" name="dcard" value="medical"><b>醫療</b>
            <input type="checkbox" id="work" name="dcard" value="work"><b>工作</b>
            <input type="checkbox" id="student" name="dcard" value="student"><b>學生</b>
            <input type="checkbox" id="read" name="dcard" value="read"><b>閱讀</b>
            <input type="checkbox" id="supernatural" name="dcard" value="supernatural"><b>靈異</b>
            <input type="checkbox" id="area" name="dcard" value="area"><b>地區</b>
            <br>
            起始頁數:<input type="text" id="start-page" name="start-page" size="2">
            結束頁數:<input type="text" id="end-page" name="end-page" size="2">
            <br>
            <input type="checkbox" id="save-data" name="save-data">
            <label for="save-data">儲存資料到 MySQL</label>
            <br>
            <button>開始</button>
            <form action="/table" method="POST">
                <input type="hidden" name="data" value="{{ data }}">
                <button type="submit">生成表格</button>
            </form>
        </form>
        
        
    </body>
</html>