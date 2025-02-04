from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from . import models


# DIRECTOR
@api_view(http_method_names=["GET"])
def directors_list_api_view(request):
   # Step 1: Collect data from DB (QuerySet)
   directors = models.Director.objects.all()
   
   # Step 2: Reformat (Serialize) QuerySet to List of dictionaries
   data = DirectorSerializer(instance=directors, many=True).data #many if list
   # print(data)
   
   # Step 3: Response data and status(default 200)
   return Response(data=data) # return Response(data={'list': data}) - так можно форматировать


@api_view(["GET"]) # http_method_names итак первое значение
def directors_detail_api_view(request, id):
   
   try:
      director = models.Director.objects.get(id=id) # DoesNotExist / MultiValueKeyError
   except models.Director.DoesNotExist:
      return Response(data={'Error': 'Director not found!'}, status=status.HTTP_404_NOT_FOUND)
   
   data = DirectorSerializer(director).data # many по дефолту False 
   
   return Response(data=data)


# MOVIE
@api_view(["GET"])
def movies_list_api_view(request):
   movies = models.Movie.objects.all()
   
   data = MovieSerializer(instance=movies, many=True).data
   
   return Response(data=data)


@api_view(["GET"])
def movies_detail_api_view(request, id):

   try:
      movie = models.Movie.objects.get(id=id)
   except models.Movie.DoesNotExist:
      return Response(data={'Error': 'Movie not found!'}, status=status.HTTP_404_NOT_FOUND)
   
   data = MovieSerializer(movie).data
   
   return Response(data=data)


# REVIEW
@api_view(["GET"])
def reviews_list_api_view(request):
   reviews = models.Review.objects.all()
   data = ReviewSerializer(instance=reviews, many=True).data
   return Response(data=data)

@api_view(["GET"])
def reviews_detail_api_view(request, id):
                            
   try:
      review = models.Review.objects.get(id=id)
   except models.Review.DoesNotExist:
      return Response(data={'Error': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)
   
   data = ReviewSerializer(review).data
   return Response(data=data)