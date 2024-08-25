from django.contrib import admin
from .models import CustomUser, Message, Article, Chat, Product, ProductImage, Category, Status, Level

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'adress', 'country', 'city')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'text', 'timestamp')
    search_fields = ('sender__username', 'text')
    list_filter = ('chat', 'sender', 'timestamp')

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1  # Определяет количество дополнительных пустых форм для сообщений в интерфейсе

class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin', 'created_at')  # Поля для отображения в списке чатов
    list_filter = ('admin', 'created_at')  # Фильтры для администрирования
    search_fields = ('user__username', 'admin__username')  # Поля для поиска
    inlines = [MessageInline]  # Встраивание сообщений в интерфейс чата

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Количество дополнительных полей для загрузки изображений
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name']
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'level', 'category']
    search_fields = ['name',]
    inlines = [ProductImageInline]
    
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)