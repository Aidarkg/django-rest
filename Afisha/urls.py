from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("movie_app.urls")),
    path('api/v1/cbv/', include("class_based_views.urls")),
    
]
