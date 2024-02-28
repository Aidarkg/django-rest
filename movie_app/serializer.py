from rest_framework import serializers
from movie_app import models

class DirectorSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Director
        fields = '__all__'

    def get_movies(self, director):
        movies = director.movie.all()
        if movies:
            return ', '.join([movie.title for movie in movies])
        else:
            return "No movies"

    def get_movies_count(self, director):
        return director.movie.count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'text', 'stars']


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = '__all__'


    def get_directors(self, movie):
        directors = movie.directors.all()
        if directors.exists():
            return ', '.join([director.name for director in directors])
        else:
            return 'No directors'
        

    def get_rating(self, movie):
        total_stars = sum(review.stars for review in movie.review.all())
        num_reviews = movie.review.count()
        if num_reviews > 0:
            return total_stars / num_reviews
        else:
            return 0.0
