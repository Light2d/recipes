from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm, UserProfileForm, LessonForm, AvatarForm
from .models import Chat, Article, CustomUser, Product, Category, Lesson
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
import random
import string
from django.core.mail import send_mail
from django.db.models import Count

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
    # chat, created = Chat.objects.get_or_create(user=request.user)
    
    form = MessageForm()  
    # messages = chat.messages.all()
    context = {
        'form': form,
        # 'messages': messages,
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

@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = AvatarForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Avatar updated successfully'})
            return JsonResponse({'errors': form.errors}, status=400)

    else:
        form = AvatarForm(instance=user)

    books = user.user_products.all()
    total_products = Product.objects.count()
    added_books = books.count()
    remaining_books = total_products - added_books
    upcoming_lessons = Lesson.objects.filter(user=user, status='upcoming').count()
    past_lessons = Lesson.objects.filter(user=user, status='past').count()
    lessons = Lesson.objects.filter(user=user)

    context = {
        'user': user,
        'books': books,
        'total_products': total_products,
        'added_books': added_books,
        'remaining_books': remaining_books,
        'upcoming_lessons': upcoming_lessons,
        'past_lessons': past_lessons,
        'form': form,
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

@login_required
def products(request):
    products = Product.objects.all()
    categories = Category.objects.prefetch_related('products').all()
    bestProducts = Product.objects.annotate(num_images=Count('images')).filter(num_images__gt=0).order_by('?')[:6]

    if request.method == "POST":
        if 'add_to_my_books' in request.POST:
            product_id = request.POST.get('product_id')
            if product_id:
                try:
                    product = Product.objects.get(pk=product_id)
                    request.user.user_products.add(product)
                except Product.DoesNotExist:
                    # Логируем или обрабатываем ошибку
                    print(f"Product with id {product_id} does not exist.")
            # Перенаправляем на ту же страницу или другую, если необходимо
            return redirect('my_books')
        
    return render(request, 'products.html', {'products': products, 'categories': categories, 'bestProducts': bestProducts})


@login_required
def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    
    if request.method == "POST":
        if 'add_to_my_books' in request.POST:
            request.user.user_products.add(product)
            # Перенаправляем на ту же страницу или другую, если необходимо
            return redirect('my_books')

    products = Product.objects.filter()
    otherProducts = Product.objects.exclude(pk=product_id)
    return render(request, 'product.html', {'product': product, 'products': products, 'otherProducts': otherProducts})

@login_required
def my_products(request):
    user = request.user
    user_products = user.user_products.all()
    return render(request, 'my_books.html', {'user_products': user_products})

def aboutUs(request):
    return render(request, 'aboutUs.html')

@login_required
def lesson(request):
    lessons = Lesson.objects.filter(user=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.user = request.user
            lesson.save()
            print(f"Lesson created: {lesson}")  # Отладочное сообщение
            return redirect('lesson')
        else:
            print(form.errors)  
    else:
        form = LessonForm()
    return render(request, 'lesson.html', {'form': form, 'lessons': lessons})

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@login_required
def payment(request, plan_type):
    if request.method == 'POST':
        # Получаем данные из формы
        email = request.POST.get('email')
        first_name = request.POST.get('name')
        last_name = request.POST.get('lastname')
        phone_number = request.POST.get('phone')
        address = request.POST.get('adress')
        city = request.POST.get('city')

        # Генерация случайного логина и пароля
        random_username = generate_random_string()
        random_password = generate_random_string(12)  # Длина пароля 12 символов

        # Установка статуса в зависимости от выбранного уровня
        if plan_type == 'beginner':
            status = 'paid_beginner'
        elif plan_type == 'basic':
            status = 'paid_basic'
        elif plan_type == 'pro':
            status = 'paid_pro'
        else:
            status = 'not_paid'

        # Создание нового пользователя с указанными данными
        new_user = CustomUser.objects.create_user(
            username=random_username,
            password=random_password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            adress=address,
            city=city,
            status=status
        )

        # Формирование сообщения
        subject = 'Your Account Details'
        message = (
            f"Dear {first_name} {last_name},\n\n"
            f"Your account has been successfully created.\n\n"
            f"Username: {random_username}\n"
            f"Password: {random_password}\n\n"
            f"Please keep this information safe.\n\n"
            
        )

        # Отправка письма
        send_mail(
            subject,
            message,
            'lighttt2d@gmail.com',  # Отправитель (ваш email)
            [email],  # Получатель (email пользователя)
            fail_silently=False,
        )

        return redirect('login')

    return render(request, 'payment.html', {'plan_type': plan_type})


