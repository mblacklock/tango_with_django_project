from django.conf.urls import url
from rango import views

app_name ='rango'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^about/',views.about_page,name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category,name='show_category'),
    url(r'^page/(?P<page_name_slug>[\w\-]+)/$',views.show_page,name='show_page'),
    url(r'^add_category/$', views.add_category,name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/',views.add_page,name='add_page'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/', views.profile, name='profile'),
    url(r'^profiles/$', views.list_profiles, name='list_profiles'),
]
