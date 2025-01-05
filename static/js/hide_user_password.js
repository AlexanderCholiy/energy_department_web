// JavaScript для изменения видимости пароля и иконки
document.getElementById('hide-password-current').addEventListener('click', function() {
    togglePasswordVisibility('currentPassword', this);
});

document.getElementById('hide-password-new').addEventListener('click', function() {
    togglePasswordVisibility('password', this);
});

document.getElementById('hide-password-confirm').addEventListener('click', function() {
    togglePasswordVisibility('confirmPassword', this);
});

// Функция для переключения видимости пароля
function togglePasswordVisibility(fieldId, icon) {
    var passwordField = document.getElementById(fieldId);

    if (passwordField.type === 'password') {
        passwordField.type = 'text'; // Показать пароль
        icon.className = 'bx bx-lock-open-alt'; // Поменять иконку на открытую
    } else {
        passwordField.type = 'password'; // Скрыть пароль
        icon.className = 'bx bxs-lock-alt'; // Поменять иконку на закрытую
    }
}