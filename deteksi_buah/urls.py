from django.urls import path

from . import views

urlpatterns = [
    path('', views.upGambar),#, name='index'), #views.index
    path('prediksiGambar', views.deteksiBuah),#, name='gambar'),
]