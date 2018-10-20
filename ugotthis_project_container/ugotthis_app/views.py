from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
# from django.http import HttpResponse

from .models import *


class NewUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    # setting = forms.RadioSelect


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


# def index(request):
#     return HttpResponse("Hello, world. You're at the app index.")


def homepage(request):
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request
        form = LoginForm(request.POST)

        if form.is_valid():
            # Create a new user object using the ModelForm's built-in .save()
            # giving it from the cleaned_data form.
            user = form.save()

            # As soon as our new user is created, we make this user be
            # instantly "logged in".
            auth.login(request, user)
            return redirect('/')

    else:
        # if a GET we'll create a blank form
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'pages/homepage.html', context)


def registration(request):
    # possibly need to get all default settings from db, put them in a
    # tuple (e.g., CHOICES), and assign that as value of widget:
    # CHOICES = (('1', 'First',), ('2', 'Second',))
    # choice_field = forms.ChoiceField(
    #                                   widget=forms.RadioSelect,
    #                                   choices=CHOICES
    #                                   )

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request
        form = NewUserForm(request.POST)

        if form.is_valid():
            # Create a new user object populated with the data we are
            # giving it from the cleaned_data form
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )

            # setting = UserSetting.objects.get(id=setting_id)
            # setting.selected.add(request.user)

            # As soon as our new user is created, we make this user be
            # instantly "logged in".
            auth.login(request, user)
            return redirect('/')

    else:
        # if a GET we'll create a blank form
        form = NewUserForm()

    context = {
        'form': form,
    }
    return render(request, 'pages/registration.html', context)
