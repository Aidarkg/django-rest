from django.contrib import admin
from movie_app import models


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

@admin.register(models.Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

# admin.site.register(models.Director)
# admin.site.register(models.Movie)
admin.site.register(models.Review)
