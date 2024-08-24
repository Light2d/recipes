from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm, UserProfileForm
from .models import Chat, Article, CustomUser, Product, Category
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Создаем пользователя, но не сохраняем в базу данных пока
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)  # Устанавливаем пароль
            user.save()  # Теперь сохраняем пользователя с хэшированным паролем
                
            # Аутентифицируем и входим в систему только что зарегистрированного пользователя
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Перенаправляем пользователя на главную страницу после успешной регистрации
            else:
                print("User authentication failed")  # Отладочное сообщение
        else:
            print("Form is invalid")  # Отладочное сообщение
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Перенаправить на главную страницу после входа
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def index(request):
    user = request.user
    articles = Article.objects.filter()
    products = Product.objects.filter()
    chat, created = Chat.objects.get_or_create(user=request.user)
    
    form = MessageForm()  
    messages = chat.messages.all()
    context = {
        'form': form,
        'messages': messages,
        'articles': articles,
        'products': products,
    }
    
    return render(request, "index.html", context)

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:10]  # Ограничить количество предложений
    product_list = [{
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'image': product.images.first().image.url if product.images.exists() else None  # Получаем первое изображение
    } for product in products]
    return JsonResponse({'products': product_list})


@login_required
def chat_view(request):
    chat, created = Chat.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('chat_messages.html', {
                    'chat': chat,
                    'messages': chat.messages.all(),
                    'form': form
                }, request=request)
                return JsonResponse({'html': html})
            return redirect('chat_view')
    else:
        form = MessageForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('chat/chat_messages.html', {
            'chat': chat,
            'messages': chat.messages.all(),
            'form': form
        }, request=request)
        return JsonResponse({'html': html})

    return render(request, 'chat/chat.html', {'chat': chat, 'messages': chat.messages.all(), 'form': form})


@login_required
def admin_chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all()

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('chat/admin_chat.html', {
                    'chat': chat,
                    'messages': chat.messages.all(),
                    'form': form
                }, request=request)
                return JsonResponse({'html': html})

            return redirect('chat/admin_chat_view', chat_id=chat.id)
    else:
        form = MessageForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('chat/admin_chat.html', {
            'chat': chat,
            'messages': messages,
            'form': form
        }, request=request)
        return JsonResponse({'html': html})

    return render(request, 'chat/admin_chat.html', {
        'chat': chat,
        'messages': messages,
        'form': form
    })



@login_required
def admin_chat_list_view(request):
    chats = Chat.objects.all()
    return render(request, 'chat/admin_chat_list.html', {'chats': chats})


def article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    products = Product.objects.filter()
    articles = Article.objects.filter()
    return render(request, 'article.html', {'article': article, 'articles': articles, 'products': products})

def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

import json
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt  # Для тестирования, убедитесь, что CSRF защита включена на продакшене
def update_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = UserProfileForm(data, instance=request.user)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors.get_json_data()})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def products(request):
    products = Product.objects.filter()
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'products.html', {'products': products, 'categories': categories})

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    products = Product.objects.filter()
    otherProducts = Product.objects.exclude(pk=product_id)
    return render(request, 'product.html', {'product': product, 'products': products, 'otherProducts': otherProducts})

def aboutUs(request):
    return render(request, 'aboutUs.html')