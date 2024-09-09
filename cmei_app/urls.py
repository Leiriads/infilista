from django.urls import path
from . import views

urlpatterns = [
    path('criar_cmei/', views.criar_cmei, name='criar_cmei'),
    path('listar_cmei/', views.listar_cmei, name='listar_cmei'),
    path('editar_cmei/<int:codCmei>/', views.editar_cmei, name='editar_cmei'),
    path('deletar_cmei/<int:codCmei>/', views.deletar_cmei, name='deletar_cmei'),
    path('', views.pagina_inicial, name='pagina_inicial'),
]
