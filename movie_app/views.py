import random
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from movie_app import serializer, models
from rest_framework import status
from datetime import timedelta
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse_lazy


@api_view(['GET', 'POST'])
def director_list_view(request):
    if request.method == 'GET':
        director = models.Director.objects.all()
        data = serializer.DirectorSerializer(director, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.DirectorSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_view(request, id):
    try:
        director = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Director not found'})
    if request.method == 'GET':
        data = serializer.DirectorSerializer(director).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializers = serializer.DirectorSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data=serializers.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

        director.name = request.data.get('name')
        director.save()
        return Response(data=serializer.DirectorSerializer(director).data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Director deleted"})


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        print(request.user)
        movies = models.Movie.objects.all()
        data = serializer.MovieSerializer(movies, many=True).data
        return Response(data=data)
    
    elif request.method == 'POST':
        serializers = serializer.MovieCreateUpdateSerializer(data=request.data)
        print(request.data)
        if not serializers.is_valid():
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        try:
            duration = timedelta(hours=int(duration.split(':')[0]), 
                                    minutes=int(duration.split(':')[1]), 
                                    seconds=int(duration.split(':')[2]))
        except (ValueError, TypeError, IndexError):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid duration format'})

        movie = models.Movie.objects.create(
            title=title,
            description=description,
            duration=duration
        )

        director_id = request.data.get('director_id')
        director = models.Director.objects.get(pk=director_id)
        movie.directors.add(director)

        return Response(data=serializer.MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_view(request, id):
    try:
        movie = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Movie not found'})
    if request.method == 'GET':
        data = serializer.MovieSerializer(movie).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializers = serializer.MovieSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data=serializers.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        duration_str = request.data.get('duration')
        try:
            movie.duration = timedelta(hours=int(duration_str.split(':')[0]), 
                                    minutes=int(duration_str.split(':')[1]), 
                                    seconds=int(duration_str.split(':')[2]))
        except (ValueError, TypeError, IndexError):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid duration format'})
        movie.save()
        return Response(data=serializer.MovieSerializer(movie).data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Movie deleted"})


@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        review = models.Review.objects.all()
        data = serializer.ReviewSerializer(review, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.ReviewSerializer(data=request.data)
        if serializers.is_valid():
            movie_id = request.data.get('movie_id')
            if movie_id:
                movie_instance = models.Movie.objects.get(id=movie_id)
                serializers.save(movie=movie_instance)
            else:
                serializers.save()
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, id):
    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Review not found'})
    if request.method == 'GET':
        data = serializer.ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializers = serializer.ReviewSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data=serializers.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.save()
        return Response(data=serializer.ReviewSerializer(review).data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Review deleted"})

    
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "User None"}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            phone_number = request.data.get('phone_number')

            user = User.objects.create_user(
                username=username, 
                password=password, 
                email=email,
                is_active=False)

            models.Profile.objects.create(
                user=user, 
                phone_number=phone_number)
            
            activation_link = reverse_lazy('verify_user', kwargs={'user_id': user.pk})

            send_mail(
                'Подтверждение регистрации',
                f'Перейдите по ссылке для авторизации: http://127.0.0.1:8000{activation_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
        except Exception as e:
            error_message = str(e)
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(data={"message": "User has successfully registered"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def verify_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return Response({"message": "User account has been activated successfully."})
    except User.DoesNotExist:
        return Response({"error": "User with specified ID does not exist."}, status=404)

        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_review_view(request):
    if isinstance(request.user, AnonymousUser):
        return Response(data={"message": "You are not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    
    reviews = models.Review.objects.filter(user=request.user)
    serializer = serializer.ReviewSerializer(reviews, many=True)
    return Response(data=serializer.data)