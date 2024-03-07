from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User


class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name='user_movies',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField()
    directors = models.ManyToManyField(
        Director,
        related_name='movie',
        blank=True
    )

    @property
    def count_reviews(self):
        return self.review.all().count()

    @property
    def rating(self):
        rating_avg = Review.objects.filter(movie=self).aggregate(Avg('stars'))['stars__avg']
        if rating_avg is not None:
            return round(rating_avg)
        else:
            return 1

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE, 
        related_name='user_reviews',
        null=True,
        blank=True
    )
    text = models.TextField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='review',
        null=True,
        blank=True
    )
    stars = models.IntegerField(default=1, choices = [(i, i) for i in range(6)])
    
    def __str__(self):
        return str(self.id)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone_number = models.CharField(max_length=13)
