from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from .models import *
from .permissions import custom_permission_required
from django.contrib.admin.views.decorators import staff_member_required


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


@staff_member_required
@custom_permission_required(["movie.add_movie"])
def movie_create_view(request):
    genres = Genre.objects.all()
    if request.method == 'POST':
        movie = Movie()
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.genre = get_object_or_404(Genre, id=request.POST.get('genre'))
        movie.trailer = request.FILES.get('trailer')
        movie.poster = request.FILES.get('poster')
        movie.save()
        return redirect('movie_list')
    return render(request, 'movie_create.html', {'genres': genres})



@staff_member_required
def movie_update_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    genres = Genre.objects.all()
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.genre = get_object_or_404(Genre, id=request.POST.get('genre'))
        if request.FILES.get('poster'):
            movie.poster = request.FILES.get('poster')
        if request.FILES.get('trailer'):
            movie.trailer = request.FILES.get('trailer')
        movie.save()
        return redirect('movie_list')
    return render(request, 'movie_update.html', {'movie': movie,'genres': genres})


@staff_member_required
@custom_permission_required(["movie.delete_movie"])
def movie_delete_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.soft_delete()
    return redirect('movie_list')


def seat_list_view(request, session_id):
    session = get_object_or_404(Session.objects.select_related('movie', 'hall'),id=session_id,movie__is_deleted=False,)
    seats = Seat.objects.filter(hall=session.hall).order_by('row', 'number')
    bookings = Booking.objects.filter(session=session).exclude(status='cancelled')
    booked_seat_ids = list(bookings.values_list('seat_id', flat=True))
    return render(request, 'seat_list.html', {'session': session,'seats': seats,'booked_seat_ids': booked_seat_ids})


@staff_member_required
@custom_permission_required(["movie.restore_movie"])
def movie_trash_view(request):
    movies = Movie.all_objects.filter(is_deleted=True).select_related('genre')
    return render(request, 'movie_trash.html', {'movies': movies})


@staff_member_required
@custom_permission_required(["movie.restore_movie"])
def movie_restore_view(request, movie_id):
    movie = get_object_or_404(Movie.all_objects, id=movie_id, is_deleted=True)
    if request.method == 'POST':
        movie.restore()
    return redirect('movie_trash')


@staff_member_required
@custom_permission_required(["movie.delete_movie"])
def movie_hard_delete_view(request, movie_id):
    movie = get_object_or_404(Movie.all_objects, id=movie_id, is_deleted=True)
    if request.method == 'POST':
        movie.hard_delete()
    return redirect('movie_trash')


@staff_member_required
def genre_list_view(request):
    genres = Genre.objects.all()
    return render(request, 'genre_list.html', {'genres': genres})


@staff_member_required
def genre_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Genre.objects.create(name=name)
        return redirect('genre_list')
    return render(request, 'genre_create.html')