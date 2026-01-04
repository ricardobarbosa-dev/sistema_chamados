from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from chamados.views import CustomLoginView
from .views import register
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Autenticação
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/', register, name='register'),

    # Alterar senha (usuário logado)
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_change.html',
            success_url='/password_change_done/'
        ),
        name='password_change'
    ),
    path(
        'password_change_done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html'
        ),
        name='password_change_done'
    ),

    # Reset de senha
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # Redireciona página inicial "/" para a lista de chamados
    path('', RedirectView.as_view(url='/chamados/', permanent=False)),

    # URLs do app chamados
    path('chamados/', include('chamados.urls')),
]
