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
});

document.addEventListener("DOMContentLoaded", function() {
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
        console.log(data);
        document.getElementById("username").textContent = username;

        // Получение аватара пользователя из базы данных
        fetch(`/get_avatar/${user_id}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById("avatar").src = data.avatar_url || '/static/default-avatar.png';
            });
    });
});
