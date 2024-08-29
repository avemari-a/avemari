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
    const user = tg.initDataUnsafe.user;
    const user_id = user.id;
    const username = user.username || 'Unknown';

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
        fetch(`/profile/${user_id}`)
            .then(response => response.json())
            .then(data => {
                console.log('Avatar response:', data); // Логируем ответ для отладки
                if (data.avatar_url) {
                    document.getElementById("avatar").src = data.avatar_url;
                } else {
                    document.getElementById("avatar").src = ''; // Или какой-то плейсхолдер, если нужно
                }
            })
            .catch(error => console.error('Error fetching avatar:', error)); // Логирование ошибок
    })
    .catch(error => console.error('Error registering user:', error)); // Логирование ошибок
});
