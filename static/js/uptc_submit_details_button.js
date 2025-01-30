document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("myForm");
    const submitButton = document.getElementById("submitButton");

    // Функция для проверки состояния формы
    function checkFormValidity() {
        if (form.checkValidity()) {
            submitButton.classList.remove("disabled"); // Убираем класс disabled, если форма валидна
        } else {
            submitButton.classList.add("disabled"); // Добавляем класс disabled, если форма не валидна
        }
    }

    // Добавляем обработчики событий для всех полей формы
    form.addEventListener("input", checkFormValidity);

    // Проверяем состояние формы при загрузке страницы
    checkFormValidity();
});