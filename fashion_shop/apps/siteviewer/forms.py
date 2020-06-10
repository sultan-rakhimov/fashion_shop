from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Product


class UserForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', required=True,
                                 widget=forms.TextInput(attrs={'class': 'first_name'}))
    last_name = forms.CharField(label='Last Name', required=True,
                                widget=forms.TextInput(attrs={'class': 'last_name'}))
    username = forms.CharField(label='Username', required=True,
                               widget=forms.TextInput(attrs={'class': 'username'}))
    email = forms.EmailField(label='E-mail', required=True,
                             widget=forms.EmailInput(attrs={'class': 'email'}))
    password1 = forms.CharField(
        label='Password', required=True, widget=forms.PasswordInput(attrs={'class': 'password1'}))
    password2 = forms.CharField(
        label='Confirm', required=True, widget=forms.PasswordInput(attrs={'class': 'password2'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        return user


class CreateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'image',
                  'categories', 'sizes', 'colors', 'images', 'slug',)

    def save(self, user, commit=True):
        product = super().save(commit=False)
        product.user = user
        product.save()
        return product


class UpdateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'image',
                  'categories', 'sizes', 'colors', 'images', 'slug',)

    def save(self, user, commit=True):
        product = super().save(commit=False)
        product.user = user
        product.save()
        return product
