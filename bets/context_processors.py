import pdb


def user_menu(request):
    if request.user.is_authenticated:

        user_profile = request.user.profile
        if user_profile.is_admin:
            is_admin = True
        else:
            is_admin = False

        if user_profile.is_manager:
            is_manager = True
        else:
            is_manager = False

        return {
            'user_profile': user_profile,
            'user_is_admin': is_admin,
            'user_is_manager': is_manager,
        }
    else:
        return {}

