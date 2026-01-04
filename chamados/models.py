from django.db import models
from django.contrib.auth.models import User

class Chamado(models.Model):
    STATUS_CHOICES = (
        ('aberto', 'Open'),
        ('andamento', 'In progress'),
        ('fechado', 'Closed'),
    )

    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto'
    )
    criado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chamados'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    # Novo campo para anexos
    anexo = models.FileField(
        upload_to='chamados_anexos/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titulo


class HistoricoChamado(models.Model):
    chamado = models.ForeignKey(
        Chamado,
        on_delete=models.CASCADE,
        related_name='historicos'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    status_anterior = models.CharField(max_length=20)
    novo_status = models.CharField(max_length=20)
    criado_em = models.DateTimeField(auto_now_add=True)

    lido_por = models.ManyToManyField(
        User,
        related_name='historicos_lidos',
        blank=True
    )

    def __str__(self):
        return f'{self.chamado} - {self.status_anterior} → {self.novo_status}'


class RespostaChamado(models.Model):
    chamado = models.ForeignKey(
        Chamado,
        on_delete=models.CASCADE,
        related_name='respostas'
    )
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem = models.TextField()
    criada_em = models.DateTimeField(auto_now_add=True)

    lido_por = models.ManyToManyField(
        User,
        related_name='respostas_lidas',
        blank=True
    )

    def __str__(self):
        return f'Resposta de {self.autor}'


class Notificacao(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )

    chamado = models.ForeignKey(
        Chamado,
        on_delete=models.CASCADE,
        related_name='notificacoes',
        null=True,
        blank=True
    )

    mensagem = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Chamado.STATUS_CHOICES
    )
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mensagem
