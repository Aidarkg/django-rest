from rest_framework import serializers
from movie_app import models

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Director
        fields = '__all__'

    def get_movies_count(self, director):
        return director.movie.count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'text', 'stars']


class MovieSerializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = '__all__'

    def get_rating(self, movie):
        total_stars = sum(review.stars for review in movie.reviews.all())
        num_reviews = movie.reviews.count()
        if num_reviews > 0:
            return total_stars / num_reviews
        else:
            return 0.0
