from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app import serializer, models
from rest_framework import status
from datetime import timedelta



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
        movies = models.Movie.objects.all()
        data = serializer.MovieSerializer(movies, many=True).data
        return Response(data=data)
    
    elif request.method == 'POST':
        serializers = serializer.MovieSerializer(data=request.data)
        if serializers.is_valid():
            director_id = request.data.get('director_id')
            if director_id:
                director_instance = models.Director.objects.get(pk=director_id)
                serializers.save(directors=[director_instance])
            else:
                serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


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
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.save()
        return Response(data=serializer.ReviewSerializer(review).data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Review deleted"})

    