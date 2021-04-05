from dev_connected import Dev_connected

class Host(Dev_connected):
    def __init__(self, name):

        Dev_connected.__init__(self,name)

        self.collision = 'ok'
        self.mac = 'none'
        self.data = [""] # recive information
        
    def is_host(self):
        return True

