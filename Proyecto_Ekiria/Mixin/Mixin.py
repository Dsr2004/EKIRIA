from django.shortcuts import render, redirect
from django.urls import resolve, reverse_lazy


def PermissionDecorator(permissions):
    def _default_try_value(func):
        def box(*args, **kwargs):
            try:
                request = args[0]
                for permission in permissions:
                    try:
                        if request.user.rol.permissions.get(codename=permission):
                            pass
                    except Exception as e:
                        return redirect('SinPermisos')
                result = func(*args, **kwargs)
            except:
                return permissions
            return result
        return box
    return _default_try_value


class PermissionMixin(object):
    permission_required = ''
    url_redirect = 'SinPermisos'

    def get_perms(self):
       if self.permission_required:
           return self.permission_required
        
       else:
           return self.permission_required


    def get_url_redirect(self):
        if self.url_redirect is None:
            return redirect('SinPermisos')
        return redirect(self.url_redirect)
    
    def dispatch(self, request, *args, **kwargs):
        for permission in self.get_perms():
            print(permission)
            try:
                if request.user.rol.permissions.get(codename=permission):
                    pass
            except:
                return self.get_url_redirect()
        
        return super().dispatch(request, *args, **kwargs)
