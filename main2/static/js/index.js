const popupContainer = document.getElementById('popupContainer');
const userButton = document.querySelector('.v30_186');
const sidebarItems = document.querySelectorAll('.sidebar-item');

let popupVisible = false;

function togglePopup() {
  popupVisible = !popupVisible;
  popupContainer.classList.toggle('show', popupVisible);
}

function showItemText() {
  const textElement = this.querySelector('.sidebar-item-text');
  textElement.style.display = 'block';
}

function hideItemText() {
  const textElement = this.querySelector('.sidebar-item-text');
  textElement.style.display = 'none';
}

userButton.addEventListener('click', togglePopup);

sidebarItems.forEach((item) => {
  item.addEventListener('mouseenter', showItemText);
  item.addEventListener('mouseleave', hideItemText);
});
