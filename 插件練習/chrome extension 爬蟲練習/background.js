chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'show_title') {
      const title = message.title;
      chrome.scripting.executeScript({
        target: { tabId: sender.tab.id },
        function: sendTitle,
        args: [title]
      });
    }
  });
  
  function sendTitle(title) {
    const result = document.getElementById('result');
    result.textContent = `抓取的標題：${title}`;
  }
  