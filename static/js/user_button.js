document.addEventListener('DOMContentLoaded', () => {
    const userButton = document.getElementById('userButton');
    const dropdownMenu = document.getElementById('userDropdownMenu');

    // Открытие/закрытие выпадающего меню при клике на кнопку
    userButton.addEventListener('click', (event) => {
        event.stopPropagation(); // Остановить всплытие события
        dropdownMenu.classList.toggle('show'); // Переключаем класс 'show'
    });

    // Закрытие выпадающего меню при клике вне его
    window.addEventListener('click', (event) => {
        if (!userButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('show'); // Убираем класс 'show', если клик вне кнопки и меню
        }
    });
});

document.getElementById('openModal').onclick = function() {
    document.getElementById('modal').style.display = 'block';
};

document.getElementById('cancelButton').onclick = function() {
    document.getElementById('modal').style.display = 'none';
};

// Закрытие модального окна при нажатии вне его
window.onclick = function(event) {
    if (event.target == document.getElementById('modal')) {
        document.getElementById('modal').style.display = 'none';
    }
};