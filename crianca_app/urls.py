from django.urls import path
from . import views

urlpatterns = [
    path('criar_crianca/', views.criar_crianca, name='criar_crianca'),
    path('listar_crianca/', views.listar_crianca, name='listar_crianca'),
    path('editar_crianca/<int:codCrianca>/', views.editar_crianca, name='editar_crianca'),
    path('deletar_crianca/<int:codCrianca>/', views.deletar_crianca, name='deletar_crianca'),

]

