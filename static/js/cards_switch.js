function showTab(tabId) {
    // Скрыть все табы
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.style.display = 'none';
    });

    // Удалить активный класс у всех кнопок
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => {
        button.classList.remove('active');
    });

    // Показать выбранный таб
    document.getElementById(tabId).style.display = 'block';
    document.querySelector(`.tab-button[onclick="showTab('${tabId}')"]`).classList.add('active');
}