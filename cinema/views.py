from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User


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

