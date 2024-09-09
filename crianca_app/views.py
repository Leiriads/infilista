from django.shortcuts import render, redirect,get_object_or_404
from .forms import CriancaForm
from .models import Crianca
from django.utils import timezone
from django.contrib import messages
from utils import  cmei_ou_admin_requerido

@cmei_ou_admin_requerido
def criar_crianca(request):
    usuario_autenticado = request.user
    if request.method == 'POST':
        form = CriancaForm(request.POST)
        if form.is_valid():
            crianca = form.save(commit=False)
            crianca.dataInicialCadastro = timezone.now().date()  # Define a data atual
            crianca.nomeUsuario = request.user.username  # Define o nome do usuário autenticado
            crianca.save()
            messages.success(request, 'Criança cadastrada com sucesso!')
            return redirect('listar_crianca')
        
    if request.method == 'GET':
        form = CriancaForm()
    
    return render(request, 'criar_crianca.html', {'form': form,'usuario_autenticado': usuario_autenticado})

@cmei_ou_admin_requerido
def listar_crianca(request):
    usuario_autenticado = request.user
    if request.method == 'GET':
        criancas = Crianca.objects.all()
        return render(request, 'listar_crianca.html',{'criancas':criancas,'usuario_autenticado': usuario_autenticado})

@cmei_ou_admin_requerido
def editar_crianca(request, codCrianca):
    usuario_autenticado = request.user
    crianca = get_object_or_404(Crianca, codCrianca=codCrianca)
    
    if request.method == 'POST':
        form = CriancaForm(request.POST, instance=crianca)
        if form.is_valid():
            crianca = form.save(commit=False)
            # Atualiza a dataFinalCadastro com a data atual
            crianca.dataFinalCadastro = timezone.now().date()
            crianca.save()
            messages.success(request, 'Cadastro Alterado com sucesso!')
            return redirect('listar_crianca')
    else:
        form = CriancaForm(instance=crianca)
    
    return render(request, 'editar_crianca.html', {'form': form,'usuario_autenticado': usuario_autenticado})
    
@cmei_ou_admin_requerido
def deletar_crianca(request,codCrianca):
    # view chamou a model pra verificar se a crianca tem no banco
    crianca = get_object_or_404(Crianca,codCrianca = codCrianca)
    # verificou e continou 
    # a model deletou dentro do banco pela orm
    crianca.delete()
    # a model retorna pra  view

    # a minha view gerou um template ou me redirecionou pra
    messages.success(request, 'Criança Excluida com sucesso!')
    return redirect('listar_crianca')
