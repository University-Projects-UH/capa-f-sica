from ip_attribute import IP
from mac_attribute import Mac
from layer_network.route_table import RouteTable

class DevRouteTable:
    def __init__(self,count_ports = 1):

        self.ip = [IP()] * count_ports
        self.mac = [Mac()] * count_ports

        self.table = RouteTable()
        
