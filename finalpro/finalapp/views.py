from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import UserRegistrationForm, MovieForm, ReviewForm, CategoryForm
from .models import Movie, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm
from django.contrib.auth.views import LoginView


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in user after registration
            messages.success(request, 'Welcome! Your account has been created successfully.')
            return redirect('shop:home')  # Redirect to home page or wherever appropriate
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('shop:home')  # Redirect to home page or wherever appropriate
    else:
        form = MovieForm()
    return render(request, 'add_movie_1.html', {'form': form})

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('shop:movie_detail', movie_id=movie_id)  # Redirect to movie detail page or wherever appropriate
    else:
        form = ReviewForm()
    return render(request, 'add_review_1.html', {'form': form, 'movie': movie})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('shop:home')  # Redirect to home page or wherever appropriate
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user == movie.added_by:
        movie.delete()
        messages.success(request, 'Movie deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this movie.')
    return redirect('shop:home')

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user == movie.added_by:
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('shop:movie_detail', movie_id=movie.id)  # Redirect to movie detail page
        else:
            form = MovieForm(instance=movie)
        return render(request, 'edit_movie_1.html', {'form': form, 'movie': movie})
    else:
        messages.error(request, 'You are not authorized to edit this movie.')
        return redirect('shop:movie_detail', movie_id=movie.id)



def movie_list(request, c_slug=None):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()

    if category_id:
        movies = movies.filter(category__id=category_id)

    categories = Category.objects.all()

    c_page = None
    movies_list = None
    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movies_list = Movie.objects.filter(category=c_page, available=True)
    else:
        movies_list = Movie.objects.filter(available=True)
    paginator = Paginator(movies_list, 6)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        movies = paginator.page(1)

    return render(request, 'movie_list.html', {'movies': movies, 'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    movies = Movie.objects.filter(category__id=category_id)
    return render(request, 'category_detail.html', {'category': category, 'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movie_detail_1.html', {'movie': movie})

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile_1.html', {'user': user})

def home(request, c_slug=None):
    categories = Category.objects.all()
    c_page = None
    movies_list = None
    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movies_list = Movie.objects.filter(category=c_page, available=True)
    else:
        movies_list = Movie.objects.filter(available=True)
    paginator = Paginator(movies_list, 6)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        movies = paginator.page(1)

    return render(request, 'home.html', {'categories': categories, 'movies': movies})

def custom_logout(request):
    logout(request)
    return redirect('shop:home')

def SearchResult(request):
    movies = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        if query.strip():  # Check if the query is not empty after stripping whitespace
            movies = Movie.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
        else:
            messages.error(request, 'Please enter a valid movie to search.')
        return render(request, 'search.html', {'query': query, 'movies': movies})



def edit_profile(request):
    user = request.user
    user_form = CustomUserChangeForm(instance=user)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('/profile')  # Redirect to profile page or wherever appropriate
        else:
            # Optionally, you can pass form errors to the template for display
            errors = user_form.errors
            return render(request, 'edit_profile_1.html', {'user_form': user_form, 'errors': errors})

    return render(request, 'edit_profile_1.html', {'user_form': user_form})



def user_login(request):
    print("sjhdfbsjhf")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                print("User successfully logged in.")  # Add debugging output
                return redirect('shop:home')  # Redirect to the home page
            else:
                print("Authentication failed. Invalid credentials.")  # Add debugging output
        else:
            print("Form is not valid:", form.errors)  # Add debugging output
    else:
        form = AuthenticationForm()
    return LoginView.as_view(template_name='login.html')(request, form=form)
