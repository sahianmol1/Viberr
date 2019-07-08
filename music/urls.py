from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add_album', views.add_album, name="add_album"),
    path('albums/<int:album_id>', views.detail, name="detail"),
    path('add_song/<int:album_id>/', views.add_song, name="add_song"),
    path('songs', views.all_songs, name="all_songs"),
    path('album/<int:pk>/delete', views.AlbumDelete.as_view(), name='album-delete'),
    path('song/<int:pk>/delete', views.SongDelete.as_view(), name='song-delete'),
    path('register/', views.register, name='register'),
    path('login_user', views.login_user, name='login_user'),
    path('accounts/logout', views.logout_user, name='logout_user'),
    path('songs/<int:song_id>', views.favorite, name='favorite'),
    path('albums/<int:album_id>/', views.favourite_album, name='favourite_album'),
    path('albums/<int:album_id>/songs/<int:song_id>', views.favourite, name='favourite'),
    path('albums/<int:album_id>/songs/<int:song_id>/delete', views.det_song_delete, name='det_song_delete'),
]