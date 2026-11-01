from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from .models import *

def register_view(request):
    if request.user.is_authenticated:
        return redirect('movie_list')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('movie_list')
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=identifier).first()
            if user:
                username = user.username
            else:
                username = identifier
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('movie_list')
            form.add_error(None, 'Неправильный логин или пароль')
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('movie_list')


def movie_list_view(request):
    movies = Movie.objects.select_related('genre').prefetch_related('sessions')
    genres = Genre.objects.all()
    return render(request, 'movie_list.html', {'movies': movies, 'genres': genres})


def movie_detail_view(request, movie_id):
    movie = get_object_or_404(Movie.objects.select_related('genre'), id=movie_id)
    sessions = movie.sessions.select_related('hall').order_by('start_time')
    return render(request, 'movie_detail.html', {'movie': movie, 'sessions': sessions})