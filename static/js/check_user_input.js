function checkFormValidity() {
    const firstNameInput = document.getElementById('firstName');
    const lastNameInput = document.getElementById('lastName');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const currentPasswordInput = document.getElementById('currentPassword');
    const saveButton = document.getElementById('saveButton');

    // Проверяем, заполнено ли поле нового пароля
    if (passwordInput.value) {
        // Если введен новый пароль, делаем подтверждение пароля обязательным
        confirmPasswordInput.setAttribute('required', 'required');
    } else {
        // Если новое поле пароля пустое, убираем обязательность у подтверждения
        confirmPasswordInput.removeAttribute('required');
    }

    // Проверяем, совпадают ли новый пароль и подтвержденный пароль
    if (passwordInput.value !== confirmPasswordInput.value) {
        confirmPasswordInput.setCustomValidity("Пароли не совпадают");
    } else {
        confirmPasswordInput.setCustomValidity(""); // Сбрасываем сообщение об ошибке
    }

    // Проверяем состояние кнопки "Сохранить изменения"
    const isCurrentPasswordEntered = currentPasswordInput.value !== '';
    const isPasswordEntered = passwordInput.value !== '';
    const isConfirmPasswordEntered = confirmPasswordInput.value !== '';
    
    // Проверяем, совпадают ли новый пароль и подтверждение пароля
    const isPasswordMatch = passwordInput.value === confirmPasswordInput.value;

    // Кнопка доступна если:
    // 1) Введен текущий пароль
    // 2) Либо:
    //    - Имя или фамилия введены
    //    - Новый пароль введен и совпадает с подтверждением, если введен
    const isNameOrLastNameEntered = firstNameInput.value.trim() !== '' || lastNameInput.value.trim() !== '';

    if (isCurrentPasswordEntered && 
        (isNameOrLastNameEntered || 
        (isPasswordEntered && isConfirmPasswordEntered && isPasswordMatch))) {
        saveButton.removeAttribute('disabled');
        saveButton.setAttribute('aria-disabled', 'false');
    } else {
        // Если условия не выполнены, отключаем кнопку
        saveButton.setAttribute('disabled', 'true');
        saveButton.setAttribute('aria-disabled', 'true');
    }
}

// Инициализируем состояние кнопки при загрузке формы
document.addEventListener('DOMContentLoaded', checkFormValidity);