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
