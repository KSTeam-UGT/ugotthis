from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the app index.")
