from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('PaginaJuego', views.desarollador, name='desarollador'),
    path('extras', views.extras, name='extras'),
    path('descarga', views.descarga, name='descarga'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('desarrollador/', views.desarollador, name='desarrollador'),
    path('index2/',views.index2, name= 'inicio2'),
    path('usuarios/pdf/', views.exportar_usuarios_pdf, name='usuarios_pdf'),
]