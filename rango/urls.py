from django.conf.urls import url
from rango import views

app_name ='rango'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^about/',views.about_page,name='about'),
]
