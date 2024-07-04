from django.shortcuts import render, redirect, get_object_or_404
from .forms import CriancaForm
from .models import Crianca
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def cadastrar_crianca(request):
    if request.method == 'POST':
        form = CriancaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_criancas')  # Redireciona para a página de lista de crianças após salvar
    else:
        form = CriancaForm()
    
    return render(request, 'cadastrar_crianca.html', {'form': form})

@login_required
def editar_crianca(request, id):
    crianca = get_object_or_404(Crianca, id=id)
    
    if request.method == 'POST':
        form = CriancaForm(request.POST, instance=crianca)
        if form.is_valid():
            form.save()
            return redirect('lista_criancas')
    else:
        form = CriancaForm(instance=crianca)
    
    return render(request, 'editar_crianca.html', {'form': form, 'crianca': crianca})

@login_required
def lista_criancas(request):
    criancas = Crianca.objects.all().order_by('idade')
    return render(request, 'lista_criancas.html', {'criancas': criancas})

@login_required
def deletar_crianca(request, id):
    crianca = get_object_or_404(Crianca, id=id)
    crianca.delete()
    return redirect('lista_criancas')

@login_required
def sair(request):
    logout(request)
    return redirect('login')
