from django import forms
from django.contrib.auth.models import User
from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_title', 'music', 'is_favourite']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
