
const body = document.querySelector('body');
const sidebar = body.querySelector('.sidebar');
const toggle = body.querySelector('.toggle');
const searchBtn = body.querySelector('.search-box');
const modeSwitch = body.querySelector('.toggle-switch');
const modeText = body.querySelector('.mode-text');
const loginBtn = body.querySelector('.login');
const popupContainer = body.querySelector('.popup-container');

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

loginBtn.addEventListener('click', () => {
    popupContainer.classList.toggle('close');
});

body.addEventListener('click', () => {
    popupContainer.classList.remove('close');
});
