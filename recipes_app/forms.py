from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .models import Message


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = CustomUser
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }
        

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username'}))
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': 'Password'}))


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите сообщение...'}),
        }