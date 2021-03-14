from dev_connected import Dev_connected

class Hub(Dev_connected):
    def __init__(self, name, count_ports):

        Dev_connected.__init__(self,name,count_ports)