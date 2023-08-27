chrome.runtime.oninstalled.addListener(async () =>{
    const url = chrome.runtime.getUrl('hello.html');
    const tab = await chrome.tab.creat({url});
    console.log('created tab $(tab.id)');
})