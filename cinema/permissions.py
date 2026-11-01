from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login


def custom_login_required(view_func):
    def has_perm(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return has_perm


def custom_permission_required(req_permissions: list):
    def wrapper(view_func):
        def has_perm(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not request.user.has_perms(req_permissions):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return has_perm
    return wrapper