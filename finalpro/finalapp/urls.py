from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin
from django.urls import path, include
from .views import home

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('add-movie/', views.add_movie, name='add_movie'),
    path('add-review/<int:movie_id>/', views.add_review, name='add_review'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('edit-movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('movies/', views.movie_list, name='movie_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.SearchResult, name='SearchResult'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
