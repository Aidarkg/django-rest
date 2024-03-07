from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from movie_app.models import Review, Movie, Director
from movie_app.serializer import ReviewSerializer, MovieSerializer, DirectorSerializer, LoginSerializer, \
      RegisterSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from movie_app import models
from django.contrib.auth.models import User, AnonymousUser
from rest_framework import status
from rest_framework.response import Response



class MovieListApiView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination
    filterset_fields = ['title', 'description']


class MovieUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'



class ReviewListApiView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    

class RewieUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class DirectorListApiView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination


class DirectorUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User has successfully registered"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyApiView(APIView):
      def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.is_active = True
            user.save()
            return Response({"message": "User account has been activated successfully."})
        except User.DoesNotExist:
            return Response({"error": "User with specified ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        

class RewiewUserApiView(APIView):
    def get(self, request):
        if isinstance(request.user, AnonymousUser):
            return Response(data={"message": "You are not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    
        reviews = models.Review.objects.filter(user=request.user)
        serializers = ReviewSerializer(reviews, many=True)
        return Response(data=serializers.data)