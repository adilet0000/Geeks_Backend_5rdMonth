from django.contrib import admin
from django.urls import path
from movie_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/directors/", views.directors_list_create_api_view), # GET->list, POST->create 
    path("api/v1/directors/<int:id>/", views.directors_detail_api_view), # GET->item, PUT->update, DELETE->delete 
    path("api/v1/movies/", views.movies_list_create_api_view),
    path("api/v1/movies/<int:id>/", views.movies_detail_api_view),
    path('api/v1/movies/reviews/', views.movie_reviews_list),
    path("api/v1/reviews/", views.reviews_list_create_api_view),
    path("api/v1/reviews/<int:id>/", views.reviews_detail_api_view),
]