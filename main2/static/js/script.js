
const body = document.querySelector('body');
const sidebar = body.querySelector('.sidebar');
const toggle = body.querySelector('.toggle');
const searchBtn = body.querySelector('.search-box');
const modeSwitch = body.querySelector('.toggle-switch');
const modeText = body.querySelector('.mode-text');
const loginBtn = body.querySelector('.l');
const loginWindow = body.querySelector('.login-window');

toggle.addEventListener('click', () => {
    sidebar.classList.toggle('close');
});

searchBtn.addEventListener('click', () => {
    sidebar.classList.remove('close');
});

modeSwitch.addEventListener('click', () => {
    body.classList.toggle('dark');

    if (body.classList.contains('dark')) {
        modeText.textContent = '亮色模式';
    } else {
        modeText.textContent = '深色模式';
    }
});

function passDataFromFlask(user) {
    console.log(user.id);
    console.log(user.password);
    console.log(user.name);
    console.log(user.email);
    console.log(user.birthday);
}

var request = new XMLHttpRequest();
request.open('GET', '/get_user_data', true);
request.onreadystatechange = function() {
    if (request.readyState === 4 && request.status === 200) {
        var user = JSON.parse(request.responseText);
        passDataFromFlask(user);
    }
};
request.send();