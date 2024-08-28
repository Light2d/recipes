document.querySelector('.burger__icon').addEventListener('click', function() {
    const mobileMenu = document.querySelector('.header__mobile-menu');

    if (!mobileMenu.classList.contains('active')) {
        mobileMenu.style.display = 'block';
        setTimeout(() => {
            mobileMenu.classList.add('active');
            document.body.classList.add("_lock")
        }, 10); // Небольшая задержка для плавного перехода
    } else {
        mobileMenu.classList.remove('active');
        setTimeout(() => {
            mobileMenu.style.display = 'none';
            document.body.classList.remove("_lock")
        }, 300); // Время совпадает с transition
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const suggestionsList = document.getElementById('suggestions-list');

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        if (query.length > 0) {
            fetch(`/search-products/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsList.innerHTML = ''; // Очистить предыдущие предложения
                    if (data.products.length > 0) {
                        suggestionsList.style.display = 'block'; // Показать список предложений
                        data.products.forEach(product => {
                            const listItem = document.createElement('li');

                            // Проверяем, есть ли у продукта изображение
                            const productImage = product.image ? `<img src="${product.image}" alt="${product.name}" style="width: 40px; height: 40px; object-fit: cover; margin-right: 10px;">` : ' ';
                            const productPrice = `<span style="margin-left: auto;"> ${product.price} $</span>`;
                            
                            // Создаем ссылку на страницу продукта
                            listItem.innerHTML = `<a href="/product/${product.id}/" style="display: flex; align-items: center; text-decoration: none; color: inherit;">
                                                     ${productImage} ${product.name}
                                                 </a>`;

                            suggestionsList.appendChild(listItem);
                        });
                    } else {
                        suggestionsList.style.display = 'none'; // Скрыть список, если предложений нет
                    }
                });
        } else {
            suggestionsList.style.display = 'none'; // Скрыть список, если строка поиска пуста
        }
    });

    // Закрыть список при клике вне строки поиска и списка
    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !suggestionsList.contains(event.target)) {
            suggestionsList.style.display = 'none';
        }
    });
});

