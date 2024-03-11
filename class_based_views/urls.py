from django.urls import path
from class_based_views import views


urlpatterns = [
    path('movies/', views.MovieListApiView.as_view()),
    path('movies/<int:id>/', views.MovieUpdateDeleteApiView.as_view()),
    path('reviews/', views.ReviewListApiView.as_view()),
    path('reviews/<int:id>/', views.RewiewUpdateDeleteApiView.as_view()),
    path('directors/', views.DirectorListApiView.as_view()),
    path('directors/<int:id>/', views.DirectorUpdateDeleteApiView.as_view()),
    path('register/', views.RegisterApiView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('api/v1/verify/<int:id>', views.VerifyApiView.as_view(), name='verify_users'),
    path('register2/', views.RegisterApiView2.as_view()),

]