from .models import ListaEspera
from django.shortcuts import render, redirect,get_object_or_404
from .forms import ListaEsperaForm
from cmei_app.models import CMEI

from crianca_app.models import Crianca
from django.http import JsonResponse


from django.http import HttpResponseNotFound

from turma_app.models import Turma
from django.contrib import messages
from utils import admin_requerido, cmei_ou_admin_requerido

from django.db import IntegrityError

@cmei_ou_admin_requerido
def criar_lista_espera(request):
    """
    View para criar uma nova entrada na lista de espera.

    Dependendo do método da requisição (GET ou POST), esta view realiza as seguintes ações:
    - GET: Preenche o formulário com base no CMEI selecionado e exibe o formulário.
    - POST: Processa os dados do formulário, valida e salva a nova entrada na lista de espera.
    """
    # autenticação do usuário
    usuario_autenticado = request.user

    # Obtém o valor de codCmei da URL (GET) ou do POST, garantindo que seja definido
    codCmei = request.GET.get('codCmei') or request.POST.get('codCmei')

    # Verifica se o codCmei está presente e válido
    if codCmei:
        # Busca o CMEI, se não encontrado, cmei será None
        cmei = CMEI.objects.filter(codCmei=codCmei).first()
    else:
        # Se codCmei não estiver definido, define cmei como None
        cmei = None

    if request.method == 'POST':
        # Se a requisição for POST, obtém o ID da criança
        crianca_id = request.POST.get('crianca_id')
        
        # Inicializa a variável crianca como None
        crianca = None

        # Verifica se o ID da criança foi fornecido
        if crianca_id:
            try:
                # Tenta buscar a criança pelo ID fornecido
                crianca = Crianca.objects.get(pk=crianca_id)
            except Crianca.DoesNotExist:
                # Se a criança não existir, exibe uma mensagem de erro
                messages.error(request, 'Erro: Selecione uma criança existente.')
                return redirect('criar_lista_espera')

        # Verifica se a criança está cadastrada em alguma turma dentro do mesmo CMEI
        if crianca and ListaEspera.objects.filter(crianca=crianca, turma__cmei=cmei).exists():
            # Se já cadastrada, exibe mensagem de erro e não permite o cadastro novamente
            messages.error(request, f"Erro: A criança {crianca.nomeCrianca} já está cadastrada no CMEI {cmei.nomeCmei}.")
            return redirect('criar_lista_espera')

        # Cria uma instância do formulário com os dados POST e o codCmei
        form = ListaEsperaForm(request.POST, codCmei=codCmei)

        # Verifica se o formulário é válido
        if form.is_valid():
            # Se válido, cria uma nova instância de ListaEspera, define a criança e salva
            lista_espera = form.save(commit=False)
            if crianca:
                lista_espera.crianca = crianca
            try:
                lista_espera.save()
                # Redireciona para a lista de espera após o sucesso
                messages.success(request, 'Criança inserida na fila com sucesso!')
                return redirect('listar_lista_espera')
            except IntegrityError:
                # Captura erros de integridade e exibe uma mensagem de erro
                messages.error(request, 'Erro ao salvar a entrada na lista de espera. Por favor, selecione uma criança válida e tente novamente.')
                return redirect('criar_lista_espera')
        else:
            # Se o formulário não for válido, renderiza novamente o formulário com erros
            context = {
                'form': form,
                'cmei_list': CMEI.objects.all(),
                'codCmei': codCmei,
                'usuario_autenticado': usuario_autenticado
            }
            return render(request, 'criar_lista_espera.html', context)

    else:
        # Se a requisição for GET, cria uma nova instância do formulário com o codCmei
        form = ListaEsperaForm(codCmei=codCmei)

    # Obtém a lista de todos os CMEIs para preencher o seletor de CMEI no formulário
    cmei_list = CMEI.objects.all()

    # Prepara o contexto com o formulário, a lista de CMEIs e o codCmei
    context = {
        'form': form,
        'cmei_list': cmei_list,
        'codCmei': codCmei,
        'usuario_autenticado': usuario_autenticado
    }

    # Renderiza o template com o contexto preparado
    return render(request, 'criar_lista_espera.html', context)




@cmei_ou_admin_requerido
def procurar_crianca(request):
    """
    View para buscar crianças com base em uma consulta de pesquisa.

    Obtém a consulta da requisição GET, realiza uma busca no banco de dados e retorna
    os resultados como uma resposta JSON. A pesquisa é realizada com base no nome da criança.

    Parâmetros:
    - query: string que representa a consulta de pesquisa fornecida pelo usuário.

    Retorno:
    - JSON com uma lista de crianças que correspondem à consulta de pesquisa. Cada entrada
      inclui o ID, nome, nome do responsável e CPF do responsável da criança.
    """

    # Obtém o valor da consulta de pesquisa a partir dos parâmetros GET da requisição.
    # Remove espaços em branco das extremidades e converte para minúsculas.
    query = request.GET.get('query', '').strip().lower()

    if query:
        # Se houver uma consulta de pesquisa, filtra as crianças cujo nome contém a consulta.
        # A busca é feita de forma que não distingue maiúsculas de minúsculas.
        children = Crianca.objects.filter(nomeCrianca__icontains=query)

        # Cria uma lista de dicionários contendo os detalhes das crianças encontradas.
        results = [
            {
                'id': child.pk,                         # ID da criança
                'name': child.nomeCrianca,              # Nome da criança
                'responsavel': child.nomeResponsavel,   # Nome do responsável
                'cpf_responsavel': child.cpfResponsavel # CPF do responsável
            }
            for child in children
        ]
    else:
        # Se não houver consulta de pesquisa, inicializa a lista de resultados como vazia.
        results = []

    # Se não houver resultados na lista, adiciona uma entrada padrão indicando que nenhuma criança foi encontrada.
    if not results:
        results = [{'id': None, 'name': 'Nenhuma criança encontrada'}]

    # Retorna os resultados como uma resposta JSON.
    # `safe=False` permite que o JSON não seja um dicionário (pode ser uma lista).
    return JsonResponse(results, safe=False)


@cmei_ou_admin_requerido
def listar_lista_espera(request):
    usuario_autenticado = request.user
    lista_espera = ListaEspera.objects.filter(status='nao_confirmado').order_by('crianca__nomeCrianca')
    return render(request, 'listar_lista_espera.html', {'lista_espera': lista_espera,'usuario_autenticado': usuario_autenticado})

@admin_requerido
def deletar_lista_espera(request, id):
    try:
        item = get_object_or_404(ListaEspera, pk=id)
        item.delete()
        messages.success(request, "Criança Removida da lista com sucesso.")
    except Exception as e:
        messages.error(request, 'Ocorreu um erro ao excluir a lista.')
        return redirect('listar_lista_espera')
    return redirect('listar_lista_espera')  # Redireciona para a lista de espera após exclusão
    
















def lista_espera_por_cmei(request, codCmei):
    usuario_autenticado = request.user if request.user.is_authenticated else None
    cmei = get_object_or_404(CMEI, pk=codCmei)
    
    turmas = Turma.objects.filter(cmei=cmei).prefetch_related('listaespera_set__crianca').order_by('nomeTurma')
    
    if not turmas.exists():
        return HttpResponseNotFound("Nenhuma turma encontrada para o CMEI especificado.")
    
    return render(request, 'lista_espera_por_cmei.html', {
        'cmei': cmei,
        'turmas': turmas,
        'usuario_autenticado':usuario_autenticado
    })


@admin_requerido  # Certifique-se de que somente administradores possam mudar o status
def alterar_status_lista_espera(request, id):
    item = get_object_or_404(ListaEspera, pk=id)

    # Definindo o status anterior e o novo status
    status_anterior = item.get_status_display()
    if item.status == 'nao_confirmado':  # Supondo que os valores de status sejam strings
        item.status = 'confirmado'
    else:
        item.status = 'nao_confirmado'

    novo_status = item.get_status_display()
    item.save()

    # Mensagem de sucesso exibindo a alteração de status
    messages.success(request, f"Status da criança {item.crianca.nomeCrianca} alterado de {status_anterior} para {novo_status}.")
    return redirect('listar_lista_espera')