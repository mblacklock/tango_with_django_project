from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {'boldmessage': 'I am the bold message from the context',}
    return render(request, 'rango/index.html', context)

def about_page(request):
    return HttpResponse("Rango says about page. <a href='/rango/'>Index</a>")
