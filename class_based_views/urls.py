from django.urls import path
from class_based_views import views


urlpatterns = [
    path('movies/', views.MovieListApiView.as_view()),
    path('movies/<int:id>/', views.MovieUpdateDeleteApiView.as_view()),
    path('reviews/', views.ReviewListApiView.as_view()),
    path('reviews/<int:id>/', views.RewieUpdateDeleteApiView.as_view()),
    path('director/', views.DirectorListApiView.as_view()),
    path('director/<int:id>/', views.DirectorUpdateDeleteApiView.as_view()),
    path('register/', views.RegisterApiView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('api/v1/verify/<int:user_id>', views.VerifyApiView.as_view(), name='verify_users'),

]