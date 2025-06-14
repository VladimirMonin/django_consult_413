# core/views.py
from django.shortcuts import render, HttpResponse

def landing(request):
    return HttpResponse("<h1>Главная страница</h1>")