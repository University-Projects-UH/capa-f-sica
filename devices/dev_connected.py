import os

class Dev_connected:
    def __init__(self, name,count_ports = 1):

        self.name = name
        self.count_ports = int(count_ports)
        self.list_port_connected = ['none'] * self.count_ports
        
        self.last_receive = ['none'] * self.count_ports
        self.last_send = ['none'] * self.count_ports

        # create output file 
        try:
            out = open('output/' + self.name + '.txt','w')
        except:
            os.system('mkdir output')
            out = open('output/' + self.name + '.txt','w')
        out.close()


    def is_host(self):
        return False

    def send(self, bit, port):

        # channel busy?
        if not (self.last_send[port - 1] is 'none'):
            return []
        self.last_send[port - 1] = bit

        port_send = self.list_port_connected[port - 1]

        if(port_send is 'none'):
            return []

        return [(port_send, 'r')]

    def receive(self, bit, port):

        # channel busy?
        if not (self.last_receive[port - 1] is 'none'):
            return [] 

        self.last_receive[port - 1] = bit

        return []

    def stash(self, signal_time):
        pass
        
    def output(self, time):
        out = open('output/' + self.name + '.txt','a')

        for i in range(0,self.count_ports):
            port = self.name + '_' + str(i + 1)

            if(self.last_receive[i] != 'none'):
                out.writelines(str(time) + " " + port + ' receive ' + self.last_receive[i] + "\n")

            if(self.last_send[i] != 'none'):
                out.writelines(str(time) + " " + port + ' send ' + self.last_send[i] + "\n")

    def clean(self):
        for i in range(0,self.count_ports):
            self.last_receive[i] = 'none'

        for i in range(0,self.count_ports):
            self.last_send[i] = 'none'