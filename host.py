from dev_connected import Dev_connected

class Host(Dev_connected):
    def __init__(self, name):

        Dev_connected.__init__(self,name)

        self.collision = 'ok'
        self.mac = 'none'
        # self.name = name
        # self.list_port_connected = ['none']
        # self.read_info = ['null',-1]
        # self.mk_info = ['name',-1]
