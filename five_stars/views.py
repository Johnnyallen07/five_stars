from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a page after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def purchase(request):
    return render(request, 'purchase.html')


def home_page(request):
    return render(request, 'index.html')
