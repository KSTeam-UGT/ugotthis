# pylint: disable=E1101
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
# from django.http import HttpResponse

from .models import UserSetting


class NewUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    # get all default settings from db, put them in a
    # tuple (e.g., "choices"), and assign that as value of widget:
    choices = (
        ('1', 'Focus, Success, Persistence, Determination, Motivation'),
        ('2', 'Uplift, Inspire, Happiness'),
        ('3', 'Health, Strength, Fitness'),
        ('4', 'Peace, Meditation, Zen, Gratitude, Love'),
    )
    setting = forms.ChoiceField(widget=forms.RadioSelect,
                                choices=choices)


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
            # usetting = UserSetting.objects.get(id=1)
            # usetting.add(user)
            print('NEW USER ID:', user.id)
            print('USER FORM SETTING:', form.cleaned_data['setting'])
            print(request)

            if form.cleaned_data['setting'] == '1':
                keywords = [1, 2, 3, 4, 5]
                print('IF SETTING 1')
            elif form.cleaned_data['setting'] == '2':
                keywords = [6, 7, 8]
                print('IF SETTING 2')
            elif form.cleaned_data['setting'] == '3':
                keywords = [9, 10, 11]
                print('IF SETTING 3')
            else:
                keywords = [12, 13, 14, 15, 16]
                print('IF SETTING 4')

            for kw_id in keywords:
                UserSetting.objects.create(
                    keywords=UserSetting.objects.get(id=kw_id),
                    user_id=user.id,
                )

            # setting = UserSetting.objects.get(id=setting_id) OLD SEE BELOW
            # setting.selected.add(request.user)               OLD SEE BELOW
            '''
            user = User.objects.create_user(name='asdf')

            usetting = UserSetting.objects.get(id=1)
            user.selected_setting.add(usetting) # use either this or the next
                                                # line, it doesn't matter
            usetting.selected.add(user)

            '''

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
