document.addEventListener('DOMContentLoaded', function() {
    function changeBackground(area) {
        const backgroundContainer = document.getElementById('background-container');
        if (area === 'earn') {
            backgroundContainer.style.backgroundImage = "url('/static/earn.jpg')";
            document.querySelectorAll('.earn-area').forEach(area => {
                area.style.display = 'block';
            });
        } else {
            backgroundContainer.style.backgroundImage = "url('/static/fon.jpg')";
            document.querySelectorAll('.earn-area').forEach(area => {
                area.style.display = 'none';
            });
        }
    }

    document.querySelectorAll('.clickable-area').forEach(area => {
        area.addEventListener('click', (event) => {
            event.preventDefault();
            if (area.classList.contains('earn')) {
                changeBackground('earn');
            } else if (area.classList.contains('stats')) {
                changeBackground('stats');
            } else if (area.classList.contains('home')) {
                changeBackground('home');
            } else if (area.classList.contains('play')) {
                changeBackground('play');
            } else if (area.classList.contains('friends')) {
                changeBackground('friends');
            }
        });
    });

    document.querySelectorAll('.earn-area').forEach(area => {
        area.addEventListener('click', (event) => {
            event.preventDefault();
            const link = area.getAttribute('data-link');
            if (link) {
                window.open(link, '_blank');
            }
        });
    });

    // Инициализация Telegram Web Apps SDK
    const tg = window.Telegram.WebApp;

    // Проверка на наличие данных пользователя Telegram
    if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        const user = tg.initDataUnsafe.user;
        const user_id = user.id;
        const username = user.username || 'Unknown';
        const photo_url = user.photo_url || '/static/default_avatar.png'; // Используем аватар из Telegram или аватар по умолчанию

        console.log('User ID:', user_id); // Логируем ID пользователя
        console.log('Username:', username); // Логируем имя пользователя
        console.log('Photo URL:', photo_url); // Логируем URL аватара

        // Отправляем данные для регистрации на сервер
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: user_id,
                username: username
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Register response:', data); // Логируем ответ для отладки

            // Обновляем имя пользователя и аватар на фронтенде
            document.getElementById("username").textContent = username;
            const avatarElement = document.getElementById("avatar");
            if (avatarElement && photo_url) {
                avatarElement.src = photo_url; // Подставляем аватар пользователя из Telegram
            }
        })
        .catch(error => console.error('Error:', error)); // Логирование ошибок
    } else {
        console.error('Telegram WebApp user data is not available');
    }
});
