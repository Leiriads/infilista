from django.shortcuts import redirect
from django.contrib import messages

def admin_requerido(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('/')
    return _wrapped_view

def cmei_ou_admin_requerido(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Verifica se o usuário está autenticado
        if request.user.is_authenticated:
            # Verifica se o campo is_superuser é True ou False (ou seja, se o usuário tem algum valor atribuído)
            if request.user.is_superuser is not None:
                return view_func(request, *args, **kwargs)
        
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('/')
    
    return _wrapped_view
