from django.shortcuts import render, redirect,get_object_or_404
from .forms import CMEIForm
from .models import CMEI
from django.utils import timezone
from turma_app.models import Turma
from django.db import transaction
from utils import admin_requerido
from django.contrib import messages


@admin_requerido
@transaction.atomic
def criar_cmei(request):
    usuario_autenticado = request.user
    if request.method == 'POST':
        form = CMEIForm(request.POST)
        if form.is_valid():
            # Salva o CMEI
            cmei = form.save()

            # Verifica se o CMEI foi salvo com sucesso (por exemplo, verificando o ID)
            if cmei.pk:
                # Cria as turmas, associando cada uma ao CMEI recém-salvo
                turmas = [
                    Turma(nomeTurma=f'Infantil {i}', cmei=cmei)
                    for i in range(1, 4)
                ]
                Turma.objects.bulk_create(turmas)
            messages.success(request, 'Cmei cadastrado com sucesso!')
            # Redireciona para a lista de CMEIs ou exibe uma mensagem de erro
            return redirect('listar_cmei') if cmei.pk else render(request, 'criar_cmei.html', {'form': form, 'error': 'Erro ao salvar o CMEI','usuario_autenticado': usuario_autenticado})
    else:
        form = CMEIForm()
    return render(request, 'criar_cmei.html', {'form': form,'usuario_autenticado': usuario_autenticado})

@admin_requerido
def listar_cmei(request):
    usuario_autenticado = request.user
    if request.method == 'GET':
        cmeis = CMEI.objects.all()
        return render(request, 'listar_cmei.html',{'cmeis':cmeis,'usuario_autenticado': usuario_autenticado})



def pagina_inicial(request):
    """
    - Esta view é usada para renderizar uma lista de todos os objetos CMEI e verificar se o usuário está autenticado.
    - Ela exibe a lista no template 'home_cmei_list.html'.
    - Quando o usuário clica em um card, ele é redirecionado para a URL 'fila_espera/lista_espera_by_cmei/{id}' passando o id do Cmei que deseja ver.
    """
    if request.method == 'GET':
        cmeis = CMEI.objects.all()
        usuario_autenticado = request.user if request.user.is_authenticated else None
        return render(request, 'pagina_inicial.html', {'cmeis': cmeis, 'usuario_autenticado': usuario_autenticado})


@admin_requerido
def editar_cmei(request, codCmei):
    usuario_autenticado = request.user
    cmei = get_object_or_404(CMEI, codCmei=codCmei)
    
    if request.method == 'POST':
        form = CMEIForm(request.POST, instance=cmei)
        if form.is_valid():
            cmei = form.save(commit=False)
            # Atualiza a dataFinalCadastro com a data atual
            cmei.dataFinalCadastro = timezone.now().date()
            cmei.save()
            messages.success(request, 'Cmei alterado com sucesso!')
            return redirect('listar_cmei')
    else:
        form = CMEIForm(instance=cmei)
    
    return render(request, 'editar_cmei.html', {'form': form,'usuario_autenticado': usuario_autenticado})
    
    
@admin_requerido
def deletar_cmei(request,codCmei):
    try:

        cmei = get_object_or_404(CMEI,codCmei = codCmei)
        cmei.delete()
        messages.success(request, 'Cmei excluído com sucesso!')

    except Exception as e:
        messages.error(request, 'Ocorreu um erro ao excluir o cmei.')
        return redirect('listar_cmei')

    return redirect('listar_cmei')

    
