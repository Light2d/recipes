from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


class CustomUser(AbstractUser):
    # Устанавливаем свои имена обратных связей
    groups = models.ManyToManyField(Group, verbose_name='Groups', related_name='custom_user_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    user_permissions = models.ManyToManyField(Permission, verbose_name='User permissions', related_name='custom_user_set', blank=True, help_text='Specific permissions for this user.')

    user_remaining_time = models.IntegerField(default=20)
    user_highest_bid = models.IntegerField(default=0)
    
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