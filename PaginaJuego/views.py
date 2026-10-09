
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroForm

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Inicia sesión automáticamente al registrarse
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'PaginaJuego/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'PaginaJuego/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')
def index(request):
    return render(request, 'index.html')

def desarollador(request):
    return render(request, 'PaginaJuego/desarrollador.html')

def extras(request):
    return render(request, 'PaginaJuego/extras.html')

def descarga(request):
    return render(request, 'PaginaJuego/descarga.html')
