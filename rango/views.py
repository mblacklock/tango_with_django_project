from django.shortcuts import render#, render_to_response
from django.http import HttpResponse
#from django.template import RequestContext

# Create your views here.

def index(request):
    #context = RequestContext(request)

    #context_dict = {'boldmessage': "I am the bold message from the context"}
    context = {'boldmessage': 'I am the bold message from the context',}

    #return render_to_response('rango/index.html', context_dict, context)
    return render(request, 'rango/index.html', context)
    #return HttpResponse('test')

def about_page(request):
    return HttpResponse("Rango says about page. <a href='/rango/'>Index</a>")
