from django.db import models


class Director(models.Model):
   name = models.CharField(max_length=50)
   
   def __str__(self):
      return self.name


class Movie(models.Model):
   title = models.CharField(max_length=65)
   description = models.CharField(max_length=255, blank=True)
   duration = models.PositiveIntegerField()
   director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
   
   def __str__(self):
      return self.title
   
   @property
   def get_reviews(self):
      return [i.stars for i in self.reviews.all()]

STARS = (
   (1, '*'),
   (2, '* *'),
   (3, '* * *'),
   (4, '* * * *'),
   (5, '* * * * *'),
   (6, '* * * * * *'),
   (7, '* * * * * * *'),
   (8, '* * * * * * * *'),
   (9, '* * * * * * * * *'),
   (10, '* * * * * * * * * *'),
)

class Review(models.Model):
   text = models.CharField(max_length=255)
   movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
   stars = models.IntegerField(default=5, choices=STARS)
   
   def __str__(self):
      return self.text
   
   @property
   def movie_name(self):
      return self.movie.title if self.movie else None # если бы связь была ManyToMany, тогда: return [i.title for i in self.movie.all()]
