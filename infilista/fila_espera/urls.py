from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_crianca, name='cadastrar_crianca'),
    path('editar/<int:id>/', views.editar_crianca, name='editar_crianca'),
    path('lista/', views.lista_criancas, name='lista_criancas'),
    path('deletar/<int:id>/', views.deletar_crianca, name='deletar_crianca'),
    path('sair/', views.sair, name='sair'),
]
