from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name = 'index'),
    path('brand', views.brand, name='brand'),
    path('about', views.about, name='about'),
    path('specials', views.specials, name='specials'),
    path('contact', views.contact, name='contact'),
]