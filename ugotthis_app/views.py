# pylint: disable=E1101
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib import messages

from .models import UserSetting


class NewUserForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(
                                   attrs={'id': 'id_registration_username'}
                               ))
    password = forms.CharField(widget=forms.PasswordInput(
                               attrs={'id': 'id_registration_password'}))
    email = forms.EmailField()
    choices = (
        ('1', 'Focus, Success, Persistence, Determination, Motivation'),
        ('2', 'Uplift, Inspire, Happiness'),
        ('3', 'Health, Strength, Fitness'),
        ('4', 'Peace, Meditation, Zen, Gratitude, Love'),
    )
    setting = forms.ChoiceField(widget=forms.RadioSelect,
                                choices=choices)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
                                   attrs={'id': 'id_login_username'}))
    password = forms.CharField(widget=forms.PasswordInput(
                                   attrs={'id': 'id_login_password'}))


def logout_user(request):
    logout(request)
    return redirect('/')


def homepage(request):
    if request.POST.get('submit') == 'login':

        # Create a form instance and populate it with data from the request
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')

    else:
        # if a GET we'll create a blank form
        login_form = LoginForm()

    if request.POST.get('submit') == 'register':

        # Create a form instance and populate it with data from the request
        registration_form = NewUserForm(request.POST)

        if registration_form.is_valid():
            # Create a new user object populated with the data we are
            # giving it from the cleaned_data form
            user = User.objects.create_user(
                username=registration_form.cleaned_data['username'],
                password=registration_form.cleaned_data['password'],
                email=registration_form.cleaned_data['email'],
            )

            if registration_form.cleaned_data['setting'] == '1':
                keywords = [1, 2, 3, 4, 5]
            elif registration_form.cleaned_data['setting'] == '2':
                keywords = [6, 7, 8]
            elif registration_form.cleaned_data['setting'] == '3':
                keywords = [9, 10, 11]
            else:
                keywords = [12, 13, 14, 15, 16]

            # Get default keywords from db, based on user selection
            for kw_id in keywords:
                UserSetting.objects.create(
                    keywords=UserSetting.objects.get(id=kw_id),
                    user_id=user.id,
                )

            # As soon as our new user is created, we make this user be
            # instantly "logged in".
            auth.login(request, user)
            return redirect('/')

    else:
        # if a GET we'll create a blank form
        registration_form = NewUserForm()

    context = {
        'login_form': login_form,
        'registration_form': registration_form,
    }
    return render(request, 'pages/homepage.html', context)


def registration(request):
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

            if form.cleaned_data['setting'] == '1':
                keywords = [1, 2, 3, 4, 5]
            elif form.cleaned_data['setting'] == '2':
                keywords = [6, 7, 8]
            elif form.cleaned_data['setting'] == '3':
                keywords = [9, 10, 11]
            else:
                keywords = [12, 13, 14, 15, 16]

            # Get default keywords from db, based on user selection
            for kw_id in keywords:
                UserSetting.objects.create(
                    keywords=UserSetting.objects.get(id=kw_id),
                    user_id=user.id,
                )

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
