# pylint: disable=E1101
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib import messages

import requests

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
                                choices=choices,
                                label='Choose your interests:',)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
                                   attrs={'id': 'id_login_username',
                                          'class': 'textinput '
                                                   'textInput '
                                                   'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
                                   attrs={'id': 'id_login_password',
                                          'class': 'textinput '
                                                   'textInput '
                                                   'form-control'}))


def logout_user(request):
    logout(request)
    messages.success(request, 'You’ve been logged out.')
    return redirect('/')


def homepage(request):
    if request.user.is_authenticated:
        return redirect('/users/' + str(request.user))

    if request.POST.get('submit') == 'login':

        # Create a form instance and populate it with data from the request
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/users/' + username)
            else:
                messages.warning(request, "Incorrect username or password")
                return redirect('/')

    else:
        # if a GET we'll create a blank form
        login_form = LoginForm()

    if request.POST.get('submit') == 'register':

        # Create a form instance and populate it with data from the request
        registration_form = NewUserForm(request.POST,
                                        prefix='registration-form')

        if registration_form.is_valid():

            if not User.objects.filter(
                username=registration_form.cleaned_data['username']
            ).exists() and not User.objects.filter(
                email=registration_form.cleaned_data['email']
            ).exists():
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

                auth.login(request, user)
                # As soon as our new user is created, we make this user be
                # instantly "logged in".
                messages.success(request, 'Registration successful. '
                                            'Welcome to U Got This!')
                return redirect('/users/' + str(user))

            elif User.objects.filter(
                username=registration_form.cleaned_data['username']
            ).exists() or User.objects.filter(
                email=registration_form.cleaned_data['email']
            ).exists():
                print('USER OR EMAIL EXISTS')
                messages.warning(request, 'Account already exists.')
                return redirect('/')

    else:
        # if a GET we'll create a blank form
        registration_form = NewUserForm(prefix='registration-form')

    # import IPython; IPython.embed()
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


def user_page(request, username):
    if not request.user.is_authenticated:
        print('TEST')
        messages.warning(request, "Please log in to view that page")
        return redirect('/')

    if not User.objects.filter(username=username).exists() and (
        request.user.is_authenticated
    ):
        return redirect('/users/' + request.user.username)

    user = User.objects.get(username=username)
    keywords = UserSetting.objects.order_by('-created')
    keywords_by_user = keywords.filter(user=user)

    books = []
    videos = []
    for word in keywords_by_user:
        search_string = str(word).lower()

        # Get books from OpenLibrary
        books_response_subject = requests.get(
            f'https://openlibrary.org/subjects/{word}.json'
        )
        data_subject = books_response_subject.json()

        books_by_subject = data_subject['works']
        books_by_subject_results = []
        for work in books_by_subject:
            for book in work['subject']:
                if search_string in str(book).lower():
                    books_by_subject_results.append(work['title'])
        books_by_subject_results = list(set(books_by_subject_results))

        for work in books_by_subject_results:
            for book in books_by_subject:
                if work == book['title']:
                    authors = []
                    for author in book['authors']:
                        authors.append(author['name'])
                    books.append(
                        {
                            'title': book['title'],
                            'cover_id': book['cover_id'],
                            'link_key': book['key'],
                            'authors': authors,
                        },
                    )

        # Get videos from YouTube
        response_video = requests.get(
            'https://www.googleapis.com/youtube/v3/search?'
            # 'part=snippet&maxResults=5&q=' + search_string +

            '&key=AIzaSyBXLC_j264f9ZUllnvEidYIBAVckJVI5cI'
            '&safeSearch=strict&type=video'
        )
        data_video = response_video.json()
        videos_by_search_string = data_video['items']
        for video in videos_by_search_string:
            if 'videoId' in video['id']:
                videos.append(
                    {
                        'id': video['id']['videoId'],
                        'title': video['snippet']['title'],
                        'thumbnail': video['snippet']['thumbnails']['medium']['url'],
                        'link': 'https://www.youtube.com/watch?v=' + video['id']['videoId'],
                        'description': video['snippet']['description'],
                    }
                )
                # print('https://www.youtube.com/watch?v=' + video['id']['videoId'])
        # videos = list(set(videos))



    books = sorted(books, key=lambda k: k['title'])

    context = {
        'keywords': keywords_by_user,
        'books': books,
        'videos': videos,
    }
    return render(request, 'pages/user_content.html', context)
