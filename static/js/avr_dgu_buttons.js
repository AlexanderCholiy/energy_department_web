// Получаем текущий URL
const currentUrl = window.location.href;

// Получаем элементы кнопок
const actualButton = document.getElementById('DguActualToggleButton');
const notActualButton = document.getElementById('DguNotActualToggleButton');

// Получаем URL из атрибутов кнопок
const activeUrlActual = actualButton.getAttribute('data-url-active'); // URL для актуальных ДГУ
const inactiveUrlActual = actualButton.getAttribute('data-url-inactive'); // URL для актуальных заявок

const activeUrlNotActual = notActualButton.getAttribute('data-url-active'); // URL для неактуальных ДГУ
const inactiveUrlNotActual = notActualButton.getAttribute('data-url-inactive'); // URL для неактуальных заявок

// Определяем начальное состояние кнопок в зависимости от текущего URL
let isDGUActive = currentUrl.includes(activeUrlActual);
let isDGUNotActive = currentUrl.includes(activeUrlNotActual);

// Функция для переключения состояния актуальных ДГУ
function toggleActualDGU() {
    if (isDGUActive) {
        // Если текущее состояние - актуальные ДГУ, переходим на актуальные заявки
        window.location.href = inactiveUrlActual; // Переход по ссылке для актуальных заявок
    } else {
        // Если текущее состояние - актуальные заявки, переходим на актуальные ДГУ
        window.location.href = activeUrlActual; // Переход по ссылке для актуальных ДГУ
    }
    isDGUActive = !isDGUActive; // Переключаем состояние
}

// Функция для переключения состояния неактуальных ДГУ
function toggleNotActualDGU() {
    if (isDGUNotActive) {
        // Если текущее состояние - неактуальные ДГУ, переходим на неактуальные заявки
        window.location.href = inactiveUrlNotActual; // Переход по ссылке для неактуальных заявок
    } else {
        // Если текущее состояние - неактуальные заявки, переходим на неактуальные ДГУ
        window.location.href = activeUrlNotActual; // Переход по ссылке для неактуальных ДГУ
    }
    isDGUNotActive = !isDGUNotActive; // Переключаем состояние
}
