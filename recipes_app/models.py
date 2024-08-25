from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
    STATUS_CHOICES = [
        ('paid_beginner', 'Paid Beginner'),
        ('paid_basic', 'Paid Basic'),
        ('paid_pro', 'Paid PRO'),
        ('not_paid', 'Not paid'),
        ('not_renewed', 'Not renewed'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_paid', verbose_name='Status')

    
class Chat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chats")
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="admin_chats", limit_choices_to={'is_staff': True}, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Проверка на наличие admin
        admin_username = self.admin.username if self.admin else "No Admin"
        return f"Chat between {self.user.username} and {admin_username}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Проверка на наличие sender
        sender_username = self.sender.username if self.sender else "Unknown Sender"
        return f"Message from {sender_username} in chat {self.chat.id}"

class Article(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    theme = models.TextField()
    image = models.ImageField(upload_to='articles/images/')
    background = models.ImageField(upload_to='articles/images/')
    date = models.DateField()

    def __str__(self):
        return self.name
    
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
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, related_name='products')
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, related_name='products')
    # document = models.FileField(upload_to='documents/', blank=True, null=True)
    
    def __str__(self):
        return self.name

    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name + ' Image'
    