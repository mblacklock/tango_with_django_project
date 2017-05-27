from django.shortcuts import render
from django.http import HttpResponse

from django.template.defaultfilters import slugify

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        try:
            # Checks for potential duplicate slug
            Category.objects.get(slug=slugify(request.POST["name"]))
            return render(request, 'rango/add_category.html', {'form':form,'slug_exists':True})
        except Category.DoesNotExist:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return index(request)
            else:
                print(form.errors)

    return render(request, 'rango/add_category.html', {'form':form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
##        try:
##            # Checks for potential duplicate slug
##            Page.objects.get(slug=slugify(request.POST["name"]))
##            return render(request, 'rango/add_category.html', {'form':form,'slug_exists':True})
##        except Category.DoesNotExist:
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    return render(request, 'rango/add_page.html', {'form':form, 'category': category})
