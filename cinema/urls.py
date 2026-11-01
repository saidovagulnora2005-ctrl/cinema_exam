from django.urls import path
from .views import *

urlpatterns = [
    path('', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('movie/list', movie_list_view, name='movie_list'),
    path('movies/add/',movie_create_view, name='movie_create'),
    path('movie/detail/<int:movie_id>/', movie_detail_view, name='movie_detail'),
    path('movies/<int:movie_id>/edit/', movie_update_view, name='movie_update'),
    path('movies/<int:movie_id>/delete/', movie_delete_view, name='movie_delete'),
    path('sessions/<int:session_id>/seats/',seat_list_view,name='seat_list'),
    path('movies/trash/', movie_trash_view, name='movie_trash'),
    path('movies/<int:movie_id>/restore/', movie_restore_view, name='movie_restore'),
    path('movies/<int:movie_id>/hard-delete/', movie_hard_delete_view, name='movie_hard_delete'),
]
