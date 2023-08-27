const titleElement = document.querySelector('title');
if (titleElement) {
  const title = titleElement.innerText;
  chrome.runtime.sendMessage({ action: 'show_title', title: title });
}
