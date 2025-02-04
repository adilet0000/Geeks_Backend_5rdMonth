from rest_framework import serializers
from . import models


class DirectorSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.Director
      # __all__ - не выводит функции, только поля с базы данных
      fields = "__all__" # все, или выбирать через запятую: ['id', 'title', ..], еще можно = 'id title ..'.split()
      # exclude = ['id'] - все кроме того что впишешь, функции тоже не видит как и __all__
      
class MovieSerializer(serializers.ModelSerializer):
   director = serializers.SerializerMethodField() # для показа поля name вместо id
   
   class Meta:
      model = models.Movie
      fields = "__all__"
   
   def get_director(self, object): # для показа поля name вместо id
      return object.director.name
      
class ReviewSerializer(serializers.ModelSerializer):
   movie = serializers.SerializerMethodField()
   
   class Meta:
      model = models.Review
      fields = "__all__"
      
   def get_movie(self,object):
      return object.movie.title