from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth import logout as auth_logout

from .forms import UsuarioForm
from django.http import JsonResponse


from utils import admin_requerido
from django.contrib import messages


@admin_requerido
def criar_usuario(request):
    usuario_autenticado = request.user
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('listar_usuarios')  # Redireciona para a página de login ou outra página desejada
    else:
        form = UsuarioForm()

    return render(request, 'criar_usuario.html', {'form': form,'usuario_autenticado': usuario_autenticado})




def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "GET":
        error_message = request.session.pop('login_error', None)
        return render(request, 'login.html', {'login_success': None, 'error_message': error_message})

    elif request.method == "POST":
        username = request.POST.get('username')  # Corrigido para 'username'
        senha = request.POST.get('password')     # Corrigido para 'password'
        usuario = authenticate(username=username, password=senha)
        
        if not usuario:
            request.session['login_error'] = 'Usuário ou senha inválidos'
            return JsonResponse({'success': False, 'message': 'Usuário ou senha inválidos'})
        else:
            auth_login(request, usuario)
            request.session['usuario'] = usuario.pk
            return JsonResponse({'success': True, 'message': 'Login bem-sucedido'})

    return redirect('/')


@admin_requerido
def listar_usuarios(request):
    usuario_autenticado = request.user
    usuarios = User.objects.all()  # Obtém todos os usuários do modelo User
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios,'usuario_autenticado': usuario_autenticado})


@admin_requerido
def editar_usuario(request, pk):
    usuario_autenticado = request.user
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário alterado com sucesso!')
            return redirect('listar_usuarios')  # Redireciona para a lista de usuários
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario,'usuario_autenticado': usuario_autenticado})


@admin_requerido
def excluir_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)

    # Verifique se o username do usuário é 'admin'
    if usuario.username == 'admin':
        messages.error(request, 'Este é o usuário admin e não pode ser excluído.')
        return redirect('listar_usuarios')
    
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário Excluido com sucesso!')
        return redirect('listar_usuarios')  # Redireciona para a lista de usuários


def sair(request):
    # Realiza o logout do usuário
    auth_logout(request)
    messages.success(request, 'Você escolheu sair! até logo!')
    # Redireciona para a página de login
    return redirect('/')
