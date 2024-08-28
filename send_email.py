import os
from django.core.mail import send_mail
from django.conf import settings

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipes.settings')

# Теперь можно отправлять письмо
send_mail(
    'Test Subject',
    'This is a test message.',
    'lighttt2d@gmail.com',
    ['lighttt2d@gmail.com'],
    fail_silently=False,
)
