from django.urls import path
from . import views
from chamados import views as chamados_views

urlpatterns = [
    path('', views.lista_chamados, name='lista_chamados'),  # /chamados/
    path('novo/', views.criar_chamado, name='criar_chamado'),  # /chamados/novo/
    path('editar/<int:id>/', views.editar_chamado, name='editar_chamado'),  # /chamados/editar/<id>/
    path('excluir/<int:chamado_id>/', views.excluir_chamado, name='excluir_chamado'),  # /chamados/excluir/<id>/
    path('chamado/<int:chamado_id>/status/', views.alterar_status_chamado, name='alterar_status_chamado'),  # /chamados/chamado/<id>/status/
    path('chamado/<int:id>/', views.detalhe_chamado, name='detalhe_chamado'),  # /chamados/chamado/<id>/
]

handler403 = chamados_views.erro_403
handler404 = chamados_views.erro_404
handler500 = chamados_views.erro_500
