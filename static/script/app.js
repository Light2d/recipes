document.addEventListener('DOMContentLoaded', function() {
    const chatWindow = document.getElementById('chatWindow');
    const openChat = document.getElementById('openChat');
    const closeChat = document.getElementById('closeChat');

    openChat.addEventListener('click', function() {
        chatWindow.style.display = 'flex'; // Показываем окно чата
        openChat.classList.add('hidden'); // Скрываем кнопку
    });

    closeChat.addEventListener('click', function() {
        chatWindow.style.display = 'none'; // Скрываем окно чата
        openChat.classList.remove('hidden'); // Показываем кнопку
    });
});        
