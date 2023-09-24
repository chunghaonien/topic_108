// 在網頁中執行的JavaScript函數
function runRecordedScript(eventScript) {
    // 解析事件記錄，每行一個事件
    var events = eventScript.split('\n');

    // 遍歷事件並執行
    events.forEach(function(event) {
        if (event.trim() !== '') {
            try {
                eval(event);
            } catch (error) {
                console.error('Error executing event:', error);
            }
        }
    });
}

// 此處不需要示例記錄的事件，因為事件將在Python中傳遞

// 在頁面載入後，執行記錄的事件
document.addEventListener("DOMContentLoaded", function() {
    runRecordedScript(recordedEvents); // 注意：recordedEvents 應該在Python中傳遞
});
