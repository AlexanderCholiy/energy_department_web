function showTab(tabId, event) {
    // Предотвращаем отправку формы
    if (event) {
        event.preventDefault();
    }

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
    const activeButton = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
}