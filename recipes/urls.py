
from django.contrib import admin
from django.urls import path
from recipes_app import views
from django.urls import path, include  
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('accounts/', include('allauth.urls')),    
    path('logout/', views.user_login, name='logout'),
    
    path('chat/', views.chat_view, name='chat_view'),
    path('admin_chat/', views.admin_chat_list_view, name='admin_chat_list_view'),
    path('admin_chat/<int:chat_id>/', views.admin_chat_view, name='admin_chat_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
