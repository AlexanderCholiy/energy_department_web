document.querySelectorAll('.footer-menu-item').forEach(item => {
    item.addEventListener('click', event => {
        const submenu = item.nextElementSibling; // Получаем следующее подменю

        // Закрываем все подменю, кроме текущего
        document.querySelectorAll('.footer-submenu').forEach(sub => {
            if (sub !== submenu) {
                sub.classList.remove('active'); // Убираем класс активного подменю
            }
        });

        // Переключаем класс активного подменю
        submenu.classList.toggle('active');

        // Предотвращаем закрытие подменю при клике на сам элемент
        event.stopPropagation();
    });
});

// Закрываем все подменю при клике вне их
document.addEventListener('click', () => {
    document.querySelectorAll('.footer-submenu').forEach(submenu => {
        submenu.classList.remove('active'); // Убираем класс активного подменю
    });
});
