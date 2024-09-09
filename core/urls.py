
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/',include('usuario_app.urls')),
    path('crianca/',include('crianca_app.urls')),
    path('cmei/',include('cmei_app.urls')),
    path('turma/',include('turma_app.urls')),
    path('fila_espera/',include('fila_espera_app.urls')),
    path('',include('cmei_app.urls')),
]
