from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User


class Director(models.Model):
    name = models.CharField(max_length=255, verbose_name='имя')

    class Meta:
        verbose_name = 'режиссер'
        verbose_name_plural = 'режиссеры'

    def __str__(self):
        return self.name


class Movie(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name='user_movies',
        null=True,
        blank=True,
        verbose_name='пользователь'
    )
    title = models.CharField(max_length=255, unique=True, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    duration = models.DurationField(verbose_name='продолжительность')
    directors = models.ManyToManyField(
        Director,
        related_name='movie',
        blank=True,
        verbose_name='режиссеры'
    )

    class Meta:
        verbose_name = 'фильм'
        verbose_name_plural ='фильмы'

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
        blank=True,
        verbose_name='пользователь'
    )
    text = models.TextField(verbose_name='текст')
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='review',
        null=True,
        blank=True,
        verbose_name='фильм'
    )
    stars = models.IntegerField(default=1, choices = [(i, i) for i in range(6)], verbose_name='оценка')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
    
    def __str__(self):
        return str(self.user)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='пользователь'
    )
    phone_number = models.CharField(max_length=13, verbose_name='номер телефона')

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'