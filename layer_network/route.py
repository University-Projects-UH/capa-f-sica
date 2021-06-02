
class Route():
    def __init__(self, destination, mask, gateway = '0' * 32, interface = 1):
        # ip destino
        self._destination = destination
        # mascara de red
        self._mask = mask    
        # puerta de enlace 
        self._gateway = gateway   
        # numero de puerto 
        self._interface = interface  

    def get_mask(self):
        return self._mask

    def compare(self,r2):
        """Retorna 'True' si las rutas son iguales, 'False' en caso contrario"""
        if(self._destination != r2._destination):
            return False
        if(self._mask != r2._mask):
            return False
        if(self._gateway != r2._gateway):
            return False
        if(self._interface != r2._interface):
            return False
        return True
        