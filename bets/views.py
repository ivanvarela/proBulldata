from django.shortcuts import render,redirect
from bets.utils import *
from bets.models import Profile
# Asegurar que los templatetags estén cargados
import bets.templatetags.filters

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse


# Create your views here.

@login_required(login_url='login')
def home(request):
    context = {}
    context = get_revenue_metrics(context)

    return render(request, 'bets/home.html', context)


@login_required(login_url='login')
def admin_users(request):
    lista = Profile.objects.order_by('last_name')
    context = {
        'lista': lista
    }
    return render(request, 'bets/admin.html', context)


@login_required(login_url='login')
def proc_acceso(request, profile_id):
    if request.method == 'POST':
        with transaction.atomic():
            profile = Profile.objects.get(id=profile_id)
            selected_status = request.POST.get('status')
            profile.status = selected_status
            profile.save()
            messages.success(request, f'Usuario {profile.last_name}, actualizado correctamente')

            if selected_status == "A":
                send_email(profile.user.username)

            return redirect('bets:admin_users')

    return False


@login_required(login_url='login')
def chng_admin(request, profile_id):
    if request.method == 'POST':
        profile = Profile.objects.get(id=profile_id)
        profile.is_admin = request.POST.get('is_admin') == 'True'
        profile.save()
        messages.success(request, f'Usuario {profile.last_name}, actualizado correctamente')
        return redirect('bets:admin_users')
    else:
        return redirect('bets:admin_users')




@login_required(login_url='login')
def delete_user(request, profile_id):
    """Vista de respaldo para eliminación tradicional (no HTMX)"""
    if request.method == 'POST' and request.user.profile.is_admin:
        try:
            with transaction.atomic():
                profile = Profile.objects.get(id=profile_id)

                # Verificar que no se está eliminando a sí mismo
                if profile.user == request.user:
                    messages.error(request, 'No puedes eliminarte a ti mismo')
                    return redirect('bets:admin_users')

                user = profile.user
                nombre = f"{profile.last_name}, {profile.first_name}"

                # Eliminar el perfil y el usuario
                profile.delete()
                user.delete()

                messages.success(request, f'Usuario {nombre} eliminado correctamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar usuario: {str(e)}')

    return redirect('bets:admin_users')