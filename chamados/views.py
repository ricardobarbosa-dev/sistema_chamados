from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import Chamado, HistoricoChamado, Notificacao
from .forms import RespostaChamadoForm


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


@login_required
def lista_chamados(request):
    if request.user.is_superuser:
        chamados = Chamado.objects.all()
    else:
        chamados = Chamado.objects.filter(criado_por=request.user)

    chamados_com_nao_lido = []

    for chamado in chamados:
        historico_nao_lido = chamado.historicos.exclude(
            lido_por=request.user
        ).exists()

        resposta_nao_lida = chamado.respostas.exclude(
            lido_por=request.user
        ).exists()

        chamados_com_nao_lido.append({
            'chamado': chamado,
            'nao_lido': historico_nao_lido or resposta_nao_lida
        })

    return render(request, 'chamados/lista.html', {
        'chamados_com_nao_lido': chamados_com_nao_lido
    })


@login_required
def criar_chamado(request):
    if request.method == 'POST':
        Chamado.objects.create(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            criado_por=request.user,
            anexo=request.FILES.get('anexo')  # <<< Agora suporta upload
        )
        messages.success(request, 'Ticket created successfully!')
        return redirect('lista_chamados')

    return render(request, 'chamados/novo.html')


@login_required
def editar_chamado(request, id):
    chamado = get_object_or_404(
        Chamado,
        id=id,
        **({} if request.user.is_staff else {'criado_por': request.user})
    )

    if chamado.status == 'fechado':
        messages.error(request, 'Closed tickets cannot be edited.')
        return redirect('lista_chamados')

    if request.method == 'POST':
        chamado.titulo = request.POST.get('titulo')
        chamado.descricao = request.POST.get('descricao')
        chamado.status = request.POST.get('status')

        # Atualizar anexo se enviado
        if 'anexo' in request.FILES:
            chamado.anexo = request.FILES['anexo']

        chamado.save()

        messages.success(request, 'Ticket updated successfully!')
        return redirect('lista_chamados')

    return render(request, 'chamados/editar.html', {'chamado': chamado})


@user_passes_test(lambda u: u.is_superuser)
def excluir_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    chamado.delete()
    messages.success(request, 'Ticket deleted successfully!')
    return redirect('lista_chamados')


@user_passes_test(lambda u: u.is_superuser)
def alterar_status_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if request.method == 'POST':
        novo_status = request.POST.get('status')

        if novo_status != chamado.status:
            status_anterior = chamado.status
            chamado.status = novo_status
            chamado.save()

            HistoricoChamado.objects.create(
                chamado=chamado,
                usuario=request.user,
                status_anterior=status_anterior,
                novo_status=novo_status
            )

            Notificacao.objects.create(
                usuario=chamado.criado_por,
                chamado=chamado,
                status=chamado.status,
                mensagem=(
                    f"The status of the ticket "
                    f"<b>'{chamado.titulo}'</b> "
                    f"has been changed to "
                    f"<b>{chamado.get_status_display()}</b>."
                )
            )

            messages.success(request, 'Status updated successfully!')

    return redirect('lista_chamados')


@login_required
def detalhe_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)

    if not request.user.is_staff and chamado.criado_por != request.user:
        return render(request, 'chamados/403.html', status=403)

    pode_responder = not (
        chamado.status == 'fechado' and not request.user.is_staff
    )

    for h in chamado.historicos.exclude(lido_por=request.user):
        h.lido_por.add(request.user)

    for r in chamado.respostas.exclude(lido_por=request.user):
        r.lido_por.add(request.user)

    Notificacao.objects.filter(
        usuario=request.user,
        chamado=chamado,
        lida=False
    ).update(lida=True)

    if request.method == 'POST':
        if not pode_responder:
            messages.error(request, 'This ticket is closed and cannot be replied.')
            return redirect('detalhe_chamado', id=chamado.id)

        form = RespostaChamadoForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.chamado = chamado
            resposta.autor = request.user
            resposta.save()

            if chamado.criado_por != request.user:
                Notificacao.objects.create(
                    usuario=chamado.criado_por,
                    chamado=chamado,
                    mensagem=f'New reply in ticket "{chamado.titulo}"',
                    status=chamado.status
                )

            return redirect('detalhe_chamado', id=chamado.id)
    else:
        form = RespostaChamadoForm()

    return render(request, 'chamados/detalhe_chamado.html', {
        'chamado': chamado,
        'form': form,
        'timeline': montar_timeline(chamado),
        'pode_responder': pode_responder
    })


def montar_timeline(chamado):
    eventos = []

    for h in chamado.historicos.all():
        eventos.append({
            'tipo': 'status',
            'usuario': h.usuario,
            'data': h.criado_em,
            'status_anterior': h.status_anterior,
            'novo_status': h.novo_status,
            'obj': h
        })

    for r in chamado.respostas.all():
        eventos.append({
            'tipo': 'resposta',
            'usuario': r.autor,
            'data': r.criada_em,
            'mensagem': r.mensagem,
            'obj': r
        })

    eventos.sort(key=lambda x: x['data'])
    return eventos

# errors

def erro_403(request, exception=None):
    return render(request, 'chamados/403.html', status=403)


def erro_404(request, exception=None):
    return render(request, 'chamados/404.html', status=404)


def erro_500(request):
    return render(request, 'chamados/500.html', status=500)
