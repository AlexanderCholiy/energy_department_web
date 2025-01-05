// Показываем уведомление
const alertElement = document.getElementById('notification');
alertElement.classList.add('show');

// Уведомление исчезает через 7 секунд
setTimeout(function() {
    alertElement.classList.remove('show');
    
    // Добавляем класс для анимации исчезновения
    alertElement.style.animation = 'slideOutDown var(--transition) forwards';
    setTimeout(() => alertElement.remove(), 500);
}, 7000);