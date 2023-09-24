const { exec } = require('child_process');
const fs = require('fs');

// 定義要運行的Python腳本命令
const pythonScript = 'run_python_script.js';

// 使用Node.js執行Python腳本
exec(`python ${pythonScript}`, (error, stdout, stderr) => {
  if (error) {
    console.error(`運行Python腳本時出現錯誤: ${error}`);
    return;
  }
  
  console.log('Python腳本成功運行');
  
  // 讀取事件記錄文件
  fs.readFile('event_log.txt', 'utf8', (err, data) => {
    if (err) {
      console.error(`讀取事件記錄文件時出現錯誤: ${err}`);
      return;
    }
    
    // 在這裡可以處理事件記錄數據，例如進行分析或其他操作
    console.log('事件記錄內容:');
    console.log(data);
  });
});
