from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ImageForm, SongForm, UserForm
from .models import Album, Song
from django.db.models import Q
from django.http import JsonResponse, request

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


# Create your views here.




def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        all_albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            all_albums = all_albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'all_albums': all_albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'all_albums': all_albums})


def add_album(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)

            if form.is_valid():
                album = form.save(commit=False)
                album.user = request.user
                album.album_logo = request.FILES['album_logo']
                file_type = album.album_logo.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                        'album': album,
                        'form': form,
                        'error_message': 'Image file must be PNG, JPG, or JPEG',
                    }
                    return render(request, 'music/add_album.html', context)
                album.save()
                return render(request, 'music/detail.html', {'detail': album})
        else:
            form = ImageForm()
        return render(request, 'music/add_album.html', {'form': form})


def detail(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        detail_page = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail.html', {'detail': detail_page})


def add_song(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=album_id)

        if form.is_valid():
            albums_songs = album.song_set.all()
            for s in albums_songs:
                if s.song_title == form.cleaned_data.get("song_title"):
                    context = {
                        'album': album,
                        'form': form,
                        'error_message': 'You already added that song',
                    }
                    return render(request, 'music/add_song.html', context)
            song = form.save(commit=False)
            song.album = album
            song.audio_file = request.FILES['music']
            file_type = song.music.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'music/add_song.html', context)
            song.save()
            return render(request, 'music/detail.html', {'detail': album})
        context = {
            'album': album,
            'form': form,
        }
        return render(request, 'music/add_song.html', context)


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('index')


class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('all_songs')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'all_albums': all_albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'all_albums': all_albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def all_songs(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        all_albums = Album.objects.filter(user=request.user)
        return render(request, 'music/songs.html', {'all_albums': all_albums})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)

    if song.is_favourite:
        song.is_favourite = False
    else:
        song.is_favourite = True
    song.save()
    all_albums = Album.objects.filter(user=request.user)
    return render(request, 'music/songs.html', {'all_albums': all_albums})


def favourite(request, song_id, album_id):
    song = get_object_or_404(Song, pk=song_id)

    if song.is_favourite:
        song.is_favourite = False
    else:
        song.is_favourite = True
    song.save()
    detail_page = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'detail': detail_page})


def favourite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    if album.is_favorite:
        album.is_favorite = False
    else:
        album.is_favorite = True
    album.save()
    all_albums = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'all_albums': all_albums})


def det_song_delete(request, song_id, album_id):
    song = get_object_or_404(Song, pk=song_id)
    song.delete()
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'detail': album})
