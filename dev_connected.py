class Dev_connected:
    def __init__(self, name,count_ports = 1):

        self.name = name
        self.count_ports = int(count_ports)
        self.list_port_connected = []
        for i in range(self.count_ports):
            self.list_port_connected.append('none')
        
        self.read_info = []
        self.mk_info = []
        for i in range(self.count_ports):
            self.read_info.append(['time',self.name + '_' + str(i + 1),'recive','null'])
            self.mk_info = ['name',-1]
