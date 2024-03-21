from django.contrib import admin
from .models import Category, Movie

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # This line prepopulates the slug based on the name field

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'get_category', 'added_by')
    list_filter = ('release_date', 'category')  # Updated to use 'category' instead of 'categories'
    search_fields = ('title', 'actors', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('added_by',)

    def get_category(self, obj):
        return obj.category.name if obj.category else None
    get_category.short_description = 'Category'
