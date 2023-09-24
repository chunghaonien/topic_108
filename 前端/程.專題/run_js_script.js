const fs = require('fs');

// 读取并执行event_log.txt文件的内容
try {
  const script = require('./event_log.txt');
  console.log('成功运行event_log.txt脚本');
} catch (err) {
  console.error(`执行event_log.txt脚本时出现错误: ${err}`);
}
