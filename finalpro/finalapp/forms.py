
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Review, Category
from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'trailer_link']  # Changed from 'categories' to 'category'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class CustomUserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']