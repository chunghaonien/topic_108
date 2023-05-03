<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title>取得網頁程式碼範例</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h1>取得網頁程式碼範例</h1>
        <select id='url-list'>
            <option value="bahamut">巴哈</option>
            <option value="dcard">dcard</option>
            <option value="yahoo">yahoo論壇</option>
            <option value="ptt">ptt</option>
            <option value="mobile01">mobile01</option>
            <option value="reddit">reddit</option>
            <option value="bbc">bbc</option>
        </select>
        <div id="page-content"></div>
        <label for="data">程式碼：</label>
        <br>
        <textarea id="data" name="data" rows="20" cols="80">{{ data }}</textarea>
        <br>
        <textarea id="sql_data" name="sql_data" rows="2" cols="80">{{ sql_data }}</textarea>
        <script>
            $(document).ready(function() {
                $("#url-list").on('change', function() {
                    var selectedPage = $(this).val();
                    $.ajax({
                        type: "GET",
                        url: "/web/" + selectedPage,
                        success: function(response) {
                            $("#page-content").html(response);
                        },
                        error: function(xhr, status, error) {
                            console.log(error);
                        }
                    });
                });
            });
        </script>
    </body>
</html>

