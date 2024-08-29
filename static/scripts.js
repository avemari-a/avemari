document.addEventListener('DOMContentLoaded', function() {
    function changeBackground(area) {
        const backgroundContainer = document.getElementById('background-container');
        const earnAreas = document.querySelectorAll('.earn-area');

        switch (area) {
            case 'earn':
                backgroundContainer.style.backgroundImage = "url('/static/earn.jpg')";
                earnAreas.forEach(area => area.style.display = 'block');
                break;
            default:
                backgroundContainer.style.backgroundImage = "url('/static/fon.jpg')";
                earnAreas.forEach(area => area.style.display = 'none');
                break;
        }
    }

    // Обработка кликов на основные вкладки
    document.querySelectorAll('.clickable-area').forEach(area => {
        area.addEventListener('click', event => {
            event.preventDefault();
            const areaClass = area.classList[0];
            changeBackground(areaClass);
        });
    });

    // Обработка кликов на зоны вкладки Earn
    document.querySelectorAll('.earn-area').forEach(area => {
        area.addEventListener('click', event => {
            event.preventDefault();
            const link = area.getAttribute('data-link');
            if (link) {
                window.open(link, '_blank');
            }
        });
    });

    // Инициализация Telegram Web Apps SDK
    const tg = window.Telegram.WebApp;
    const user = tg.initDataUnsafe.user;
    const user_id = user.id;
    const username = user.username || 'Unknown';

    // Отправка данных для регистрации на сервер
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id, username })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Register response:', data); // Логируем ответ для отладки
        document.getElementById("username").textContent = username;

        // Получение аватара пользователя из базы данных
        return fetch(`/profile/${user_id}`);
    })
    .then(response => response.json())
    .then(data => {
        console.log('Avatar response:', data); // Логируем ответ для отладки
        const avatarUrl = data.avatar_url || '/static/default_avatar.png'; // Путь к аватару по умолчанию
        document.getElementById("avatar").src = avatarUrl;
    })
    .catch(error => console.error('Error:', error)); // Логирование ошибок
});
