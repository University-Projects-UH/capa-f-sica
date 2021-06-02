from devices.dev_connected import Dev_connected
from tools import Tools

class Hub(Dev_connected):
    def __init__(self, info):

        name = info[0]
        count_ports = int(info[1])

        Dev_connected.__init__(self,name,count_ports)

    def receive(self, bit, port):

        # channel busy?
        if(self.last_receive[port - 1] == 'none'):
            return [] 

        self.last_receive[port - 1] = bit

        r = []
        for i in range(1,self.count_ports):
            if(i != port):
                r.append((Tools.union_name_port(self.name,i),'s'))

        return r
        