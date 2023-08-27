document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('crawlButton').addEventListener('click', function () {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const activeTab = tabs[0];
        chrome.scripting.executeScript({
          target: { tabId: activeTab.id },
          function: crawlTitle
        });
      });
    });
  });
  
  function crawlTitle() {
    chrome.scripting.executeScript({
      function: getAndShowTitle
    });
  }
  
  function getAndShowTitle() {
    const titleElement = document.querySelector('title');
    if (titleElement) {
      const title = titleElement.innerText;
      chrome.runtime.sendMessage({ action: 'show_title', title: title });
    }
  }
  