from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upGambar',views.upGambar, name='uploadGambar'),
    path('prediksiGambar', views.deteksiBuah, name='gambar'),
    path('artikel', views.artikel, name='artikel')
]