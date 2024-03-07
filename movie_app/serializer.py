from rest_framework import serializers
from movie_app import models
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate



class DirectorSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Director
        fields = 'id name movie movies_count'.split()

    def get_movie(self, director):
        movies = director.movie.all()
        if movies:
            return ', '.join([movie.title for movie in movies])
        else:
            return "No movies"

    def get_movies_count(self, director):
        return director.movie.count()


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=models.Movie.objects.all())

    class Meta:
        model = models.Review
        fields = 'id text movie stars'.split()



class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.PrimaryKeyRelatedField(queryset=models.Director.objects.all(), many=True)

    class Meta:
        model = models.Movie
        fields = 'id title description duration directors count_reviews rating'.split()



class MovieCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, required=True)
    description = serializers.CharField(required=True)
    duration = serializers.DurationField(required=True)
    director_id = serializers.IntegerField(required=True)

    def validate_director_id(self, director_id):
        if models.Director.objects.filter(id=director_id).count() == 0:
            raise ValidationError('Invalid director id')
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise ValidationError("Both username and password are required.")
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("Invalid username or password.")
        data['user'] = user
        return data


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        phone_number = validated_data['phone_number']
        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email,
            is_active=False)

        models.Profile.objects.create(
            user=user, 
            phone_number=phone_number)
        
        activation_link = reverse_lazy('verify_users', kwargs={'user_id': user.pk})

        send_mail(
            'Подтверждение регистрации',
            f'Перейдите по ссылке для авторизации: http://127.0.0.1:8000{activation_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        return user

