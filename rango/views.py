from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

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

@login_required
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

@login_required
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

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                context = {'login_error': 'disabled'}
        else:
            print("Invalid login: {0}, {1}".format(username, password))
            if User.objects.filter(username=username).exists():
                context = {'login_error': 'pass'}
            else:
                context = {'login_error': 'user'}
    else:
        context = {}
        
    return render(request, 'rango/login.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html',)
