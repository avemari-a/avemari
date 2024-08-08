document.addEventListener('DOMContentLoaded', function() {
    function changeBackground(area) {
        const backgroundContainer = document.getElementById('background-container');
        if (area === 'earn') {
            backgroundContainer.style.backgroundImage = "url('/static/earn.jpg')"; // Убедитесь, что путь правильный
            document.querySelectorAll('.earn-area').forEach(area => {
                area.style.display = 'block'; // Показываем кликабельные зоны для Earn
            });
        } else {
            backgroundContainer.style.backgroundImage = "url('/static/fon.jpg')"; // Путь к изображению по умолчанию
            document.querySelectorAll('.earn-area').forEach(area => {
                area.style.display = 'none'; // Скрываем кликабельные зоны для Earn
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
                window.open(link, '_blank'); // Открываем ссылку в новой вкладке
            }
        });
    });
});
