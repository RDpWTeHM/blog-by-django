from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLoginForm, UserRegisterForm

from utils import dbg_print


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        # redirect
    context = {
        "form": form,
        "title": "Login",
        "H1": "Login to Your Account"
    }
    return render(request, "login.html", context=context)


def logout_view(request):
    logout(request)

    form = UserLoginForm(request.POST or None)
    return render(request, "login.html",
                  {"form": form, "title": "Login", })


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()

        new_user = authenticate(
            username=user.username,
            password=password)
        login(request, new_user)

        return HttpResponseRedirect("/posts/")

    context = {
        "form": form,
        "title": "Register",
        "H1": "Register"
    }

    return render(request, "login.html", context=context)


# def login_view(request):
#     return ""


# def login_view(request):
#     return ""
