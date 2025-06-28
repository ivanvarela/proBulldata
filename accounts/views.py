import pdb
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView
from django.db import transaction
from django.core.mail import EmailMessage
import logging

from utils.email_templates import get_welcome_template
from .forms import CustomUserCreationForm
from bets.models import Profile



logger = logging.getLogger(__name__)


def registerUser(request):
    """Vista de registro alternativa (manual approval)"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                first_name = form.cleaned_data['first_name'].title()
                last_name = form.cleaned_data['last_name'].title()

                user = form.save(commit=False)
                user.first_name = first_name
                user.last_name = last_name
                user.email = user.username
                user.save()

                profile = Profile.objects.create(
                    user=user,
                    activo=True,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['username'],
                    celular=form.cleaned_data['celular'],
                )

                messages.success(request, 'Usuario Registrado, debe esperar su activación')

                # Enviar email de notificación al admin utilizando plantilla
                from utils.email_templates import get_base_template
                subject = f'NUEVO REGISTRO - {user.first_name} {user.last_name}'

                # Crear contenido del email con formato HTML
                content = f"""
                <tr>
                    <td style="padding-bottom: 20px;">
                        <h1 style="margin: 0; font-size: 24px; line-height: 30px; font-weight: bold; color: #333333;">Nuevo Usuario Registrado</h1>
                    </td>
                </tr>
                <tr>
                    <td style="padding-bottom: 20px;">
                        <p style="margin: 0; font-size: 16px; line-height: 24px;">
                            Se ha registrado un nuevo usuario en la plataforma:
                        </p>
                    </td>
                </tr>
                <tr>
                    <td style="padding-bottom: 20px;">
                        <p style="margin: 0; font-size: 16px; line-height: 24px;">
                            <strong>Nombre:</strong> {user.first_name} {user.last_name}<br>
                            <strong>Email:</strong> {user.email}<br>
                        </p>
                    </td>
                </tr>
                """

                admin_url = 'https://progra.bulldata.info/bets/admin/'
                html_message = get_base_template(
                    content=content,
                    email=user.email,
                    button_text="Aprobar Usuario",
                    button_url=admin_url
                )

                from_email = 'respuestas@bulldata.info'
                recipient_list = ['ivan.varela@gmail.com']

                email = EmailMessage(
                    subject=subject,
                    from_email=from_email,
                    body=html_message,
                    to=recipient_list)
                email.content_subtype = "html"
                email.send()

                html_message_user = get_welcome_template(user.email)
                email_user = EmailMessage(
                    subject="Nuevo Registro - Bienvenido a Bulldata Dashboard",
                    from_email=from_email,
                    body=html_message_user,
                    to=[user.email]
                )
                email_user.content_subtype = "html"
                email_user.send()

            return redirect('cms:home')
        else:
            messages.error(request, 'Ha ocurrido un error usuario no creado')
            for e in form.errors:
                messages.error(request, e)
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/sign-up.html', {'form': form})


def login_view(request):
    """Vista de login principal - utiliza plantilla actualizada"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Verificar que el usuario existe
            user_exists = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado, debe registrarse')
            return render(request, 'accounts/sign-in.html')

        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                if profile.is_admin or profile.status == 'A':
                    next_url = request.GET.get('next', 'bets:home_bets')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Usuario no activo, hable con el administrador')
                    logout(request)
            except Profile.DoesNotExist:
                # Si no tiene perfil, redirigir a crear uno
                return redirect('register')
        else:
            messages.error(request, 'Usuario o password incorrecto')

    return render(request, 'accounts/sign-in.html')


@login_required
def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.success(request, "Sesión cerrada")
    return redirect('cms:home')


class CustomPasswordResetView(PasswordResetView):
    """Vista personalizada para reset de contraseña"""
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = '/accounts/reset_password_done/'

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        from utils.email_templates import get_password_reset_template
        from django.template import loader

        # Obtener datos del contexto
        token = context.get('token')
        uid = context.get('uid')
        domain = context.get('domain')
        protocol = context.get('protocol')
        user = context.get('user')

        # Construir URL de restablecimiento
        reset_url = f"{protocol}://{domain}/accounts/reset/{uid}/{token}/"

        # Generar contenido HTML usando la plantilla definida en email_templates.py
        html_content = get_password_reset_template(to_email[0], reset_url)

        # Establecer asunto en español
        subject = "Restablecer tu contraseña de Bulldata Dashboard"

        # Enviar correo
        email_message = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=to_email
        )
        email_message.content_subtype = "html"
        email_message.send()


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """Vista personalizada para confirmar reset de contraseña"""
    template_name = 'accounts/reset_password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uidb64'] = self.kwargs.get('uidb64')
        context['token'] = self.kwargs.get('token')
        return context
