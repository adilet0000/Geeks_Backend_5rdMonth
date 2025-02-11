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
   director = serializers.SerializerMethodField() # для показа поля name вместо id
   
   class Meta:
      model = models.Movie
      fields = "id title description duration director get_reviews rating".split()
   
   def get_director(self, object): # для показа поля name вместо id
      if object.director.id: # подстраховочка
         return object.director.name
      return None

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
   # movie = serializers.SerializerMethodField() # лучше это делать в моделях, так как их можно будет переиспользовать
   
   class Meta:
      model = models.Review
      fields = "id text stars movie_name".split()
      
   # def get_movie(self,object):
   #    return object.movie.title