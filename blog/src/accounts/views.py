from django.shortcuts import render

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLoginForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        # redirect
    return render(request, "login.html",
                  {"form": form, "title": "Login", })


def register_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

    return render(request, "login.html",
                  {"form": form, "title": "Login", })


def logout_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

    return render(request, "login.html",
                  {"form": form, "title": "Login", })


# def login_view(request):
#     return ""


# def login_view(request):
#     return ""
