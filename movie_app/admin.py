from django.contrib import admin
from movie_app import models

admin.site.register(models.Director)
admin.site.register(models.Movie)
admin.site.register(models.Review)
