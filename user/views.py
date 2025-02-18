from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from .forms import LoginForm
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': ['Неверный логин или пароль']}, status=400)
        else:
            errors = [error for field in form for error in field.errors]
            return JsonResponse({'errors': errors}, status=400)

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                return JsonResponse({'errors': ['Пользователь с таким именем уже существует.']}, status=400)

            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return JsonResponse({'success': True})

        else:
            errors = [error for field in form for error in field.errors]
            return JsonResponse({'errors': errors}, status=400)

    else:
        form = LoginForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
