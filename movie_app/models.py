from django.db import models


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
        related_name='movie'
    )

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
