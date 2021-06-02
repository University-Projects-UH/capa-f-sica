from devices.dev_route_table import DevRouteTable
from devices.hub import Hub

class Router(Hub, DevRouteTable):
    def __init__(self, info):

        Hub.__init__(self, info)

        DevRouteTable.__init__(self,self.count_ports)
        
        ####
        self.signal_count = 0

    

