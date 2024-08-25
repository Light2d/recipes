document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.payment__form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const billingValid = validateBillingInfo();
        const paymentValid = validatePaymentInfo();
        
        if (billingValid && paymentValid) {
            form.submit();
        }
    });

    function validateBillingInfo() {
        let isValid = true;

        // Поля ввода информации о платеже
        const firstName = document.querySelector('.payment__firstname');
        const lastName = document.querySelector('.payment__lastname');
        const address = document.querySelector('.payment__adress');
        const city = document.querySelector('.payment__city');
        const postal = document.querySelector('.payment__postal');
        const phone = document.querySelector('.payment__phone');
        const email = document.querySelector('.payment__email');
        
        // Чекбоксы
        const checkboxes = document.querySelectorAll('.payment__check input[type="checkbox"]');

        clearErrors([...document.querySelectorAll('.payment__inputs input'), ...checkboxes]);

        if (firstName.value.trim() === '') {
            showError(firstName, 'First name is required');
            isValid = false;
        }

        if (lastName.value.trim() === '') {
            showError(lastName, 'Last name is required');
            isValid = false;
        }

        if (address.value.trim() === '') {
            showError(address, 'Address is required');
            isValid = false;
        }

        if (city.value.trim() === '') {
            showError(city, 'City is required');
            isValid = false;
        }

        if (postal.value.trim() === '' || !/^\d{5,6}$/.test(postal.value.trim())) {
            showError(postal, 'Invalid postal code');
            isValid = false;
        }

        if (phone.value.trim() === '' || !/^\+?\d{10,15}$/.test(phone.value.trim())) {
            showError(phone, 'Invalid phone number');
            isValid = false;
        }

        if (email.value.trim() === '' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
            showError(email, 'Invalid email');
            isValid = false;
        }

        checkboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                showError(checkbox, 'This checkbox must be checked');
                isValid = false;
            }
        });

        return isValid;
    }

    function validatePaymentInfo() {
        let isValid = true;

        const cardNumber = document.querySelector('.card__input');
        const cardMonth = document.querySelector('.card__month');
        const cardYear = document.querySelector('.card_year');
        const cardCvv = document.querySelector('.card__cvv');

        clearErrors([cardNumber, cardMonth, cardYear, cardCvv]);

        const cardNumberValue = cardNumber.value.replace(/\s+/g, '');

        if (cardNumberValue === '' || !/^\d{16}$/.test(cardNumberValue)) {
            showError(cardNumber, 'Invalid card number. Must be 16 digits.');
            isValid = false;
        }

        if (cardMonth.value === '') {
            showError(cardMonth, 'Select a month');
            isValid = false;
        }

        if (cardYear.value === '') {
            showError(cardYear, 'Select a year');
            isValid = false;
        }

        if (cardCvv.value.trim() === '' || !/^\d{3,4}$/.test(cardCvv.value.trim())) {
            showError(cardCvv, 'Invalid CVV. Must be 3 or 4 digits.');
            isValid = false;
        }

        return isValid;
    }

    function showError(input, message) {
        const parent = input.parentElement;
        let errorDiv = parent.querySelector('.error-message');

        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.classList.add('error-message');
            parent.appendChild(errorDiv);
        }

        errorDiv.textContent = message;
        input.classList.add('error');
    }

    function clearErrors(inputs) {
        inputs.forEach(input => {
            if (input) {
                const parent = input.parentElement;
                const error = parent.querySelector('.error-message');
                if (error) {
                    parent.removeChild(error);
                }
                input.classList.remove('error');
            }
        });
    }

    // Добавляем обработчики для полей, чтобы позволить ввод только цифр
    function addNumericOnlyListener(selector) {
        const field = document.querySelector(selector);
        if (field) {
            field.addEventListener('input', function () {
                this.value = this.value.replace(/\D/g, '');
            });
        }
    }

    addNumericOnlyListener('.payment__postal');
    addNumericOnlyListener('.card__input');
    addNumericOnlyListener('.payment__phone');
    addNumericOnlyListener('.card__cvv');
});
