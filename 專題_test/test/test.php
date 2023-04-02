<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>取得網頁程式碼範例</title>
    </head>
    <body>
        <h1>取得網頁程式碼範例</h1>
        <label for="url-input">請輸入網址：</label>
        <input type="text" id="url-input" value="https://www.google.com/">
        <br>
        <button onclick="getCode()">開始</button>
        <br>
        <label for="code-output">程式碼：</label>
        <br>
        <textarea id="code-output" rows="20" cols="80"></textarea>
        <script>
        async function getCode() {
            const url = document.getElementById("url-input").value;
            const headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
            };
            const request = new Request(url, { headers });

            try {
            const response = await fetch(request);
            const data = await response.text();
            const codeOutput = document.getElementById("code-output");
            codeOutput.value = data;
            } catch (error) {
            console.error(error);
            codeOutput.value = "發生錯誤：" + error.message;
            }
        }
        </script>
    </body>
</html>
