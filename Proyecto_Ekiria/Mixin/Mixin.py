from django.shortcuts import render, redirect
from django.urls import resolve, reverse_lazy




class PermissionMixin(object):
    permission_required = ''
    url_redirect = 'SinPermisos'

    def get_perms(self):
       if self.permission_required:
           return self.permission_required
        
       else: return self.permission_required


    def get_url_redirect(self):
        if self.url_redirect is None:
            return redirect('SinPermisos')
        return redirect(self.url_redirect)

    def dispatch(self, request, *args, **kwargs):
        # if request.user.has_perm(self.get_perms()):
        #     # print(request.user.has_perm('citasds'))
        
        #     user = request.user
        #     print(user)
        for permission in self.get_perms():
            try:
                if request.user.rol.permissions.get(codename=permission):
                    pass
            except:
                return self.get_url_redirect()
        
        return super().dispatch(request, *args, **kwargs)
