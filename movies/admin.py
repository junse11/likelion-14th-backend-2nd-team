from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'genre', 'release_year']
    list_filter = ['genre', 'release_year']
    search_fields = ['title', 'director']
