from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_points', views.get_points, name='points')
]