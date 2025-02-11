from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from movie_app.serializers import DirectorSerializer, MovieSerializer, MovieAndReviewsSerializer, ReviewSerializer
from . import models


# DIRECTOR
@api_view(http_method_names=["GET", "POST"])
def directors_list_create_api_view(request):
   if request.method == "GET":
      # Step 1: Collect data from DB (QuerySet)
      directors = models.Director.objects.prefetch_related('movies').all()
      
      # Step 2: Reformat (Serialize) QuerySet to List of dictionaries
      data = DirectorSerializer(instance=directors, many=True).data #many if list
      # print(data)
      
      # Step 3: Response data and status(default 200)
      return Response(data=data) # return Response(data={'list': data}) - так можно форматировать
   
   elif request.method == 'POST':
      # CREATE
      # step 1: Receive data from RequestBody
      name = request.data.get('name')
      # step 2: Create
      director = models.Director.objects.create(
         name=name
      )
      # step 3: Return response as data and status
      return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"]) # http_method_names итак первое значение
def directors_detail_api_view(request, id):
   
   try:
      director = models.Director.objects.get(id=id) # DoesNotExist / MultiValueKeyError
   except models.Director.DoesNotExist:
      return Response(data={'Error': 'Director not found!'}, status=status.HTTP_404_NOT_FOUND)
   
   if request.method == "GET":
      data = DirectorSerializer(director).data
      
      return Response(data=data)

   elif request.method == "PUT":
      director.name = request.data.get("name")
      director.save()
      return Response(status=status.HTTP_201_CREATED)
   
   elif request.method == "DELETE":
      director.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
      

# MOVIE
@api_view(["GET", "POST"])
def movies_list_create_api_view(request):
   if request.method == 'GET': 
      movies = models.Movie.objects.select_related('director').prefetch_related('reviews').all() # select для foreignkey, prefetch для manytomany (btw лучше foreignkey, он не создает доп таблицу - меньше нагрузки)
      
      data = MovieSerializer(instance=movies, many=True).data
      
      return Response(data=data)

   elif request.method == 'POST':
      serializer = MovieSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def movies_detail_api_view(request, id):
   try:
      movie = models.Movie.objects.get(id=id)
   except models.Movie.DoesNotExist:
      return Response(data={'Error': 'Movie not found!'}, status=status.HTTP_404_NOT_FOUND)
   
   if request.method == "GET":
      data = MovieSerializer(movie).data
      return Response(data=data)
   elif request.method == "PUT":
      serializer = MovieSerializer(movie, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   elif request.method == "DELETE":
      movie.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)



# для movies/reviews
@api_view(['GET'])
def movie_reviews_list(request):
   movies = models.Movie.objects.select_related('director').prefetch_related('reviews').all()
   serializer = MovieAndReviewsSerializer(movies, many=True)
   return Response(serializer.data)

# REVIEW
@api_view(["GET", "POST"])
def reviews_list_create_api_view(request):
   if request.method == "GET":
      reviews = models.Review.objects.all()
      data = ReviewSerializer(reviews, many=True).data
      return Response(data=data)

   elif request.method == "POST":
      serializer = ReviewSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()  # Сохраняем отзыв
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   # elif request.method == "POST":
   #    text = request.data.get('text')
   #    movie = request.data.get('movie') # id
   #    stars = request.data.get('stars') # int
      
   #    review = models.Review.objects.create(
   #       text=text,
   #       movie=movie,
   #       stars=stars
   #    )
      
   #    return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def reviews_detail_api_view(request, id):
                            
   try:
      review = models.Review.objects.get(id=id)
   except models.Review.DoesNotExist:
      return Response(data={'Error': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)

   if request.method == "GET":
      data = ReviewSerializer(review).data
      return Response(data=data)

   elif request.method == "PUT":
      serializer = ReviewSerializer(review, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   elif request.method == "DELETE":
      review.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)