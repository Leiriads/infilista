from django.urls import path
from . import views

urlpatterns = [
    path('criar_usuario/', views.criar_usuario, name='criar_usuario'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
    path('sair/', views.sair, name='sair'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('editar_usuario/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('excluir_usuario/excluir/<int:pk>/', views.excluir_usuario, name='excluir_usuario'),
    #path('updat ou delete/<int:id>/', views.nome_da_view, name='nome'),
]
