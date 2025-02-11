from rest_framework import serializers
from . import models


class DirectorSerializer(serializers.ModelSerializer):
   movies_count = serializers.SerializerMethodField()
   
   class Meta:
      model = models.Director
      # __all__ - не выводит функции, только поля с базы данных
      fields = "id name movies_count".split() # __all__ - все, или выбирать через запятую: ['id', 'title', ..], еще можно = 'id title ..'.split()
      # exclude = ['id'] - все кроме того что впишешь, функции тоже не видит как и __all__
      
   def get_movies_count(self, object):
      return object.movies.count()
   
   

class MovieSerializer(serializers.ModelSerializer):
   director = serializers.PrimaryKeyRelatedField(
      queryset=models.Director.objects.all()  # для POST-запросов id
   )
   director_name = serializers.CharField(source='director.name', read_only=True)  # для GET-запросов имя
   
   class Meta:
      model = models.Movie
      fields = ['id', 'title', 'description', 'duration', 'director', 'director_name', 'get_reviews']

   # def get_director(self, object): # для показа поля name вместо id
   #    if object.director.id: # подстраховочка
   #       return object.director.name
   #    return None

class MovieAndReviewsSerializer(serializers.ModelSerializer):
   rating = serializers.SerializerMethodField()
   
   class Meta:
      model = models.Movie
      fields = "id title get_reviews rating".split()
   
   def get_rating(self, object):
      reviews = object.reviews.all()
      if reviews.exists():
         return round(sum([i.stars for i in reviews]) / len(reviews), 1)
      return 0
      
      
      
      
class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(
        queryset=models.Movie.objects.all()  # Для POST и PUT (ожидаем ID фильма)
    )
    movie_title = serializers.CharField(source='movie.title', read_only=True)  # Для GET (выводим название фильма)

    class Meta:
        model = models.Review
        fields = ['id', 'text', 'stars', 'movie', 'movie_title']