from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages

def view_login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            messages.error(request, f"Login Error")
            return render(request, 'login.html')

        login(request, user)
        messages.success(request, f"Logged in Successfully")
        return redirect("/rooms")

def view_signup(request):
    if request.method == "GET":
        return render(request, 'register.html')

    if request.method == "POST":
        if User.objects.filter(username=request.POST['username']):
            messages.error(request, "Username already defined")
            return redirect("/signup")

        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        user.save()
        login(request, user)
        messages.success(request, f"Signed up Successfully")

    return redirect("/rooms")

def view_logout(request):
    logout(request)
    messages.success(request, f"Logged out Successfully")
    return redirect("/login")
