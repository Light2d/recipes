
from django.contrib import admin
from django.urls import path
from recipes_app import views
from django.urls import path, include  
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('article/<int:article_id>/', views.article, name='article'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('payment/', views.payment, name='payment'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('accounts/', include('allauth.urls')),    
    path('logout/', views.user_login, name='logout'),
    
    path('payment/<str:plan_type>/', views.payment, name='payment'),

    path('search-products/', views.search_products, name='search_products'),
     
    path('chat/', views.chat_view, name='chat_view'),
    path('admin_chat/', views.admin_chat_list_view, name='admin_chat_list_view'),
    path('admin_chat/<int:chat_id>/', views.admin_chat_view, name='admin_chat_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
