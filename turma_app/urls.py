from django.urls import path
from . import views

urlpatterns = [
    path('criar_turma/', views.criar_turma, name='criar_turma'),
    path('listar_turma/', views.listar_turma, name='listar_turma'),
    path('editar_turma/<int:codTurma>/', views.editar_turma, name='editar_turma'),
    path('deletar_turma/<int:codTurma>/', views.deletar_turma, name='deletar_turma'),
]
