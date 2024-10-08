from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import datetime  

class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Level(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    author = models.TextField(default="without author")
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, related_name='products')
    
    STATUS_CHOICES = [
        ('available', 'available'),
        ('unavailable', 'unavailable'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unavailable', verbose_name='Status')
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    
    def __str__(self):
        return self.name

    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name + ' Image'


class CustomUser(AbstractUser):
    # Устанавливаем свои имена обратных связей
    groups = models.ManyToManyField(Group, verbose_name='Groups', related_name='custom_user_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    user_permissions = models.ManyToManyField(Permission, verbose_name='User permissions', related_name='custom_user_set', blank=True, help_text='Specific permissions for this user.')
    
    username = models.CharField(max_length=120, verbose_name='username')
    email = models.EmailField(unique=True, blank=True, verbose_name='Email Address')
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Phone Number')
    adress = models.CharField(max_length=120, blank=True, verbose_name='adress')
    country = models.CharField(max_length=50, blank=True, verbose_name='country')
    city = models.CharField(max_length=50, blank=True, verbose_name='city')
    user_products = models.ManyToManyField(Product, related_name='products_by', blank=True, verbose_name='user_products')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
                               
    STATUS_CHOICES = [
        ('paid_beginner', 'Paid Beginner'),
        ('paid_basic', 'Paid Basic'),
        ('paid_pro', 'Paid PRO'),
        ('not_paid', 'Not paid'),
        ('not_renewed', 'Not renewed'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_paid', verbose_name='Status')

    
class Lesson(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_or_skype = models.CharField(max_length=50)
    date = models.DateField()
    time = models.CharField(max_length=20)  # Изменено на текстовое поле
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')

    def save(self, *args, **kwargs):
        current_datetime = timezone.now()
        lesson_datetime = timezone.make_aware(datetime.combine(self.date, datetime.strptime(self.time.split('-')[1], '%H:%M').time()))
        
        if lesson_datetime < current_datetime:
            self.status = 'past'
        else:
            self.status = 'upcoming'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.date} {self.time} ({self.status})"

class Chat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chats", null=True, blank=True)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="admin_chats", limit_choices_to={'is_staff': True}, null=True, blank=True)
    guest_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Проверка на наличие admin
        participant = self.user.username if self.user else self.guest_name or "Guest"
        admin_username = self.admin.username if self.admin else "No admin"
        return f"Chat between {self.user.username} and {admin_username}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    sender_name = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Проверка на наличие sender
        sender = self.sender.username if self.sender else self.sender_name or "Unknown Sender"
        return f"Message from {sender} in chat {self.chat.id}"

class Article(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    theme = models.TextField()
    image = models.ImageField(upload_to='articles/images/')
    background = models.ImageField(upload_to='articles/images/')
    date = models.DateField()

    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.name}"
    
class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
