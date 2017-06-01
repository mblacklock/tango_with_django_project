from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from datetime import datetime

from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# Create your views here.

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        #visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def index(request):
    # get a list of the 5 top liked categories
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context = {'categories': category_list,
               'pages': page_list}
    
    visitor_cookie_handler(request)

    context['visits'] = request.session['visits']
    
    return render(request, 'rango/index.html', context)

def about_page(request):
    visitor_cookie_handler(request)
    context = {'visits': request.session['visits']}
    return render(request, 'rango/about.html', context)

def show_category(request, category_name_slug):
    # Gets all pages in category_name_slug and creates dict

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category).order_by('-views')

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

##def register(request):
##    registered = False
##
##    if request.method == 'POST':
##        user_form = UserForm(data=request.POST)
##        profile_form = UserProfileForm(data=request.POST)
##
##        if user_form.is_valid() and profile_form.is_valid():
##            user = user_form.save()
##
##            user.set_password(user.password)
##            user.save()
##
##            profile = profile_form.save(commit=False)
##            profile.user = user
##
##            if 'picture' in request.FILES:
##                profile.picture = request.FILES['picture']
##
##            profile.save()
##
##            registered = True
##        else:
##            print(user_form.errors, profile_form.errors)
##    else:
##        user_form = UserForm()
##        profile_form = UserProfileForm()
##
##    return render(request,
##                  'rango/register.html',
##                  {'user_form': user_form,
##                   'profile_form': profile_form,
##                   'registered': registered})
##
##def user_login(request):
##    if request.method == 'POST':
##        username = request.POST.get('username')
##        password = request.POST.get('password')
##
##        user = authenticate(username=username, password=password)
##
##        if user:
##            if user.is_active:
##                login(request, user)
##                return HttpResponseRedirect(reverse('rango:index'))
##            else:
##                context = {'login_error': 'disabled'}
##        else:
##            print("Invalid login: {0}, {1}".format(username, password))
##            if User.objects.filter(username=username).exists():
##                context = {'login_error': 'pass'}
##            else:
##                context = {'login_error': 'user'}
##    else:
##        context = {}
##        
##    return render(request, 'rango/login.html', context)
##
##@login_required
##def user_logout(request):
##    logout(request)
##    return HttpResponseRedirect(reverse('rango:index'))

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html',)

def track_url(request):
    page_id = None
    url = reverse('rango:index')
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)

@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    context = {'form':form}

    return render(request,'rango/profile_registration.html',context)

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    
    return render(request, 'rango/profile.html',
                  {'userprofile': userprofile, 'selecteduser': user, 'form': form})

@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()

    return render(request, 'rango/list_profiles.html',
                  {'userprofile_list': userprofile_list})
