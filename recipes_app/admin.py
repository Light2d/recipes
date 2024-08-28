from django.contrib import admin
from .models import CustomUser, Message, Article, Chat, Product, ProductImage, Category, Status, Level, Lesson, ContactMessage, Subscription

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0  # Убираем пустые строки для новых записей


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'adress', 'country', 'city', 'avatar')
    filter_horizontal = ('groups', 'user_products')
    inlines = [LessonInline]

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
    
class LessonAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'phone_or_skype', 'date', 'time', 'status')
    list_filter = ('status', 'user', 'date')
    search_fields = ('name', 'email', 'phone_or_skype', 'date', 'time')
    
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
    
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)