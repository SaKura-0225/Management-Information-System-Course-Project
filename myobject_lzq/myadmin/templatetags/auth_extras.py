from django.core.exceptions import PermissionDenied
from functools import wraps

def multiple_permission_required(perms):
    """
    用于检查多个权限的装饰器，perms 应为权限字符串列表
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perms(perms):
                raise PermissionDenied()
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator