from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

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

def index2(request):
    return render(request, 'index2')

@staff_member_required
def exportar_usuarios_pdf(request):
    User = get_user_model()
    usuarios = User.objects.all().order_by('username')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
    estilos = getSampleStyleSheet()
    celda = estilos['BodyText']
    celda.fontSize = 7
    celda.leading = 9

    elementos = [Paragraph("Listado de usuarios", estilos['Title']), Spacer(1, 12)]

    datos = [["Usuario", "Email", "Contraseña (hash)"]]
    for u in usuarios:
        datos.append([
            Paragraph(u.username, celda),
            Paragraph(u.email or "-", celda),
            Paragraph(u.password, celda),
        ])

    tabla = Table(datos, colWidths=[90, 140, 300], repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
    ]))
    elementos.append(tabla)

    doc.build(elementos)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    # 'inline' lo abre en el navegador para imprimir; cambia a 'attachment' para forzar descarga
    response['Content-Disposition'] = 'inline; filename="usuarios.pdf"'
    return response