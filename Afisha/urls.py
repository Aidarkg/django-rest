from django.contrib import admin
from django.urls import path
from movie_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/director_list/', views.director_list_view),
    path('api/v1/director_list/<int:id>', views.director_detail_view),
    path('api/v1/movie_list/', views.movie_list_view),
    path('api/v1/movie_list/<int:id>', views.movie_detail_view),
    path('api/v1/review_list/', views.review_list_view),
    path('api/v1/review_list/<int:id>', views.review_detail_view),
    path('api/v1/login/', views.login_view),
    path('api/v1/register/', views.register_view),
    path('api/v1/user/review/', views.user_review_view),
    path('api/v1/verify/<int:user_id>', views.verify_view, name='verify_user')

]
