from django.shortcuts import render, redirect,get_object_or_404
from .forms import TurmaForm
from .models import Turma
from django.utils import timezone
from django.contrib import messages
from utils import admin_requerido,cmei_ou_admin_requerido

@admin_requerido
def criar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o formulário se estiver válido
            messages.success(request, 'Turma cadastrada com sucesso!')
            return redirect('listar_turma')
    else:
        form = TurmaForm()

    # Se você precisar passar opções para o campo cmei, não é necessário já que o ModelChoiceField já faz isso.
    return render(request, 'criar_turma.html', {'form': form})

            

@cmei_ou_admin_requerido
def listar_turma(request):
    usuario_autenticado = request.user
    is_admin = request.user.is_superuser
    if request.method == 'GET':
        turmas = Turma.objects.all()

        # Agrupa as turmas por CMEI em um dicionário
        turmas_por_cmei = {}
        for turma in turmas:
            cmei_id = turma.cmei.codCmei  # Acessando o ID correto do CMEI
            if cmei_id not in turmas_por_cmei:
                turmas_por_cmei[cmei_id] = []
            turmas_por_cmei[cmei_id].append(turma)

        return render(request, 'listar_turma.html', {'turmas_por_cmei': turmas_por_cmei,'usuario_autenticado': usuario_autenticado,'is_admin':is_admin})



@cmei_ou_admin_requerido
def editar_turma(request, codTurma):
    turma = get_object_or_404(Turma, codTurma=codTurma)
    
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            turma.save()
            messages.success(request, 'Turma alterada com sucesso!')
            return redirect('listar_turma')
    else:
        form = TurmaForm(instance=turma)
    
    return render(request, 'editar_turma.html', {'form': form})
    
    
@cmei_ou_admin_requerido
def deletar_turma(request,codTurma):
    try:
        turma = get_object_or_404(Turma,codTurma = codTurma)
        turma.delete()
        messages.success(request, 'Turma excluída com sucesso!')
    except Exception as e:
        messages.error(request, 'Ocorreu um erro ao excluir a turma.')
        return redirect('listar_turma')
    
    return redirect('listar_turma')