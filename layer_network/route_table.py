from layer_network.route import Route
from ip_attribute import IP
from tools import Tools

class RouteTable:
    def __init__(self):
        self.table = []

    def reset(self):
        """Borra todas las rutas de la tabla"""
        self.table = []

    def add(self, route : Route):
        """Add una ruta de la tabla
        Retorna 'True' si la annadio o 'False' si no existe"""

        ind = self._search(route)
        if(ind == -1):
            return False

        # Mantener ordenada la tabla por prioridad de las mascaras
        ind_prior = self._search_priority(route.get_mask())

        self.table.insert(ind_prior, route)
        return True

    def delete(self, route : Route):
        """Elimina una ruta de la tabla.
        Retorna 'True' si la elimino o 'False' si no existe"""

        ind = self._search(route)

        if(ind == -1):
            return False
        
        self.table.pop(ind)
        return True

    def _search(self, route : Route):
        """Retorna el indice en la tabla de la ruta especificada, o '-1' si no existe"""
        for i in range(0,len(self.table)):
            if(self.table[i].compare(route)):
                return i

        return -1

    def _search_priority(self, mask):
        """Indice donde colocar a 'mask' en la tabla ordenada por prioridad"""
        for i in range(0,len(self.table)):
            if(self.table[i].get_mask() < mask):
                return i

        return len(self.table)
        
    def routing(self, ip_target : IP):
        
        for r in self.table:
            mask_normalize = IP.ip_normalize(r.mask)
            aux = Tools.and_strings(ip_target.get_ip_bin(), mask_normalize)

            if(aux == IP.ip_normalize(r.destination)):
                return [True,r.interface,r.gateway]

        return [False]