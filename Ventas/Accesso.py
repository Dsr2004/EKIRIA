
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
             
class accesoCatalogo():
    def __init__(self, usuario):
        self.usuario = usuario

    def DefinirGrado(self):
        try:
            grados = self.usuario.rol.permissions.filter(name__icontains="Puede visualizar elementos de grado").order_by('id')
            MayorGrado = 1
            for i in grados:
                # codename = Grado x, name=puede visualizar dfddf x 
                iteracion = int(i.codename[6:])
                if iteracion > MayorGrado:
                    MayorGrado = iteracion
                    
            return {'gradoMayor': "Grado {}".format(MayorGrado), 'permisos':grados, "gradoNumero":MayorGrado}
                
        except:
            return False
        
    