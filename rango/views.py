from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page

# Create your views here.

def index(request):
    # get a list of the 5 top liked categories
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context = {'categories': category_list,
               'pages': page_list}
    
    return render(request, 'rango/index.html', context)

def about_page(request):
    return render(request, 'rango/about.html', )

def show_category(request, category_name_slug):
    # Gets all pages in category_name_slug and creates dict

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context = {
            'pages': pages,
            'category': category
            }

    except:
        context = {
            'pages': None,
            'category': None
            }

    return render(request, 'rango/category.html', context)

def show_page(request, page_name_slug):
    # 

    try:
        page = Page.objects.get(slug=page_name_slug)

        context = {
            'page': page,
            }

    except:
        context = {
            'page': None,
            }

    return render(request, 'rango/page.html', context)
