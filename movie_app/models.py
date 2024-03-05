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
        rating_avg = Review.objects.filter(movie=self).aggregate(Avg('stars'))['stars__avg']
        if rating_avg is not None:
            return round(rating_avg)
        else:
            return 1

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='review'
    )
    stars = models.IntegerField(default=1, choices = [(i, i) for i in range(6)])
    
    def __str__(self):
        return self.movie.title
