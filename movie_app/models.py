from django.db import models
from django.db.models import Avg


class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField()
    directors = models.ManyToManyField(
        Director,
        related_name='movie',
        null=True,
        blank=True
    )

    @property
    def count_reviews(self):
        return self.review.all().count()

    @property
    def rating(self):
        return Review.objects.filter(movie=self).aggregate(Avg('stars'))

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='review'
    )
    stars = models.IntegerField(default=1, null=True)

    def __str__(self):
        return self.movie.title
