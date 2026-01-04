from .models import Notificacao 

def notificacoes_nao_lidas(request):
    if request.user.is_authenticated:
        return {
            'notificacoes_nao_lidas': request.user.notificacoes.filter(lida=False),
            'total_notificacoes': request.user.notificacoes.filter(lida=False).count()
        }
    return {}

def notificacoes_usuario(request):
    if request.user.is_authenticated:
        notificacoes = request.user.notificacoes.order_by('-criada_em')[:5]
        nao_lidas = request.user.notificacoes.filter(lida=False).count()
    else:
        notificacoes = []
        nao_lidas = 0

    return {
        'notificacoes': notificacoes,
        'notificacoes_nao_lidas': nao_lidas
    }