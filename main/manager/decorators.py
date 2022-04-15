from django.core.exceptions import PermissionDenied

def role_required(allowed=[]):
    def decorator(view_func):
        def wrap(request,*args,**kwargs):
            if request.user.is_manager:
                return view_func(request,*args,**kwargs)
            else:
                raise PermissionDenied

        return wrap
    return decorator