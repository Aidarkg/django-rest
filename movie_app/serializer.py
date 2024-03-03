from rest_framework import serializers
from movie_app import models


class DirectorSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Director
        fields = 'id name movies movies_count'.split()

    def get_movies(self, director):
        movies = director.movie.all()
        if movies:
            return ', '.join([movie.title for movie in movies])
        else:
            return "No movies"

    def get_movies_count(self, director):
        return director.movie.count()


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    class Meta:
        model = models.Review
        fields = 'id text movie stars'.split()

    def get_movie(self, review):
        return review.movie.title


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = 'id title description duration directors count_reviews rating'.split()

    def get_directors(self, movie):
        directors = movie.directors.all()
        if directors.exists():
            return ', '.join([director.name for director in directors])
        else:
            return 'No directors'
