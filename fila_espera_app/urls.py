from django.urls import path
from . import views

urlpatterns = [
    path('criar_lista_espera/', views.criar_lista_espera, name='criar_lista_espera'),
    path('listar_lista_espera/', views.listar_lista_espera, name='listar_lista_espera'),
    path('deletar_lista_espera/<int:id>/', views.deletar_lista_espera, name='deletar_lista_espera'),
    path('lista_espera_por_cmei/<int:codCmei>/', views.lista_espera_por_cmei, name='lista_espera_por_cmei'),
    path('procurar_crianca/', views.procurar_crianca, name='procurar_crianca'),
    path('alterar-status-lista-espera/<int:id>/', views.alterar_status_lista_espera, name='alterar_status_lista_espera'),


]