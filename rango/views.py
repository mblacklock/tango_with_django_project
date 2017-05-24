from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Rango says hellow world. <a href='/rango/about'>About</a>")

def about_page(request):
    return HttpResponse("Rango says about page. <a href='/rango/'>Index</a>")
