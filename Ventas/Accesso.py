
class acceso():
    def __init__(self, usuario):
        self.usuario = usuario
        
    def esEmpleado(self):
        try:
            if self.usuario.rol.permissions.get(codename="Empleado"):
                return True
            else:
                return False
        except:
           return False
    def esClente(self):
        try:
            if self.usuario.rol.permissions.get(codename="Cliente"):
                return True
            else:
                return False
        except:
            return False
        
    def esAdministrador(self):
        try:
            if self.usuario.rol.permissions.get(codename="Administrador"):
                return True
            else:
                return False
        except:
            return False