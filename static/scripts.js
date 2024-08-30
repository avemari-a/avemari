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
    if (window.Telegram && window.Telegram.WebApp) {
        const tg = window.Telegram.WebApp;
        const user = tg.initDataUnsafe && tg.initDataUnsafe.user;
        
        if (user) {
            const user_id = user.id;
            const username = user.username || 'Unknown';

            console.log('User ID:', user_id); // Логируем ID пользователя
            console.log('Username:', username); // Логируем имя пользователя

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

                document.getElementById("username").textContent = username;

                // Получение аватара пользователя из базы данных
                return fetch(`/profile/${user_id}`);
            })
            .then(response => response.json())
            .then(data => {
                console.log('Avatar response:', data); // Логируем ответ для отладки
                const avatarElement = document.getElementById("avatar");
                if (avatarElement) {
                    if (data.avatar_url) {
                        console.log('Avatar URL:', data.avatar_url); // Логируем URL аватара
                        avatarElement.src = data.avatar_url;
                    } else {
                        console.log('Avatar URL is missing, using default'); // Логируем использование аватара по умолчанию
                        avatarElement.src = '/static/default_avatar.png'; // Путь к аватару по умолчанию
                    }
                } else {
                    console.error('Avatar element not found');
                }
            })
            .catch(error => console.error('Error:', error)); // Логирование ошибок
        } else {
            console.error('Telegram WebApp user data is not available');
        }
    } else {
        console.error('Telegram WebApp SDK is not loaded');
    }
});
