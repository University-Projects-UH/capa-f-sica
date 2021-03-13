from host import Host
from hub import Hub

SIGNAL_TIME = 10

class MyProtocol():
    def __init__(self, filename):
        self.filename = filename
        self.host_list = []
        self.hub_list = []
        self.name_dict = {}

    def read_file(self):
        return open(self.filename, 'r') #Read script.txt

    def get_device_name(self, port):
        name = ''
        for c in port:
            if(c == '_'):
                break
            name += c

        return name

    def get_device_port_index(self, port):
        port_index = ''
        len_port = len(port)
        for i in range(len(port)):
            if(port[len_port - i - 1] == '_'):
                break
            port_index += port[len_port - i - 1]

        return int(port_index[::-1])

    def get_device(self, par):
        if(par[0] == 0): #is a host
            return self.host_list[par[1]]
        return self.hub_list[par[1]] #is a hub

    def create_instruction(self, strings_line): #create devices
        device = strings_line[2]
        if(device == 'host'):
            assert(len(strings_line) - 3 == 1), 'Host should only have name'
            self.name_dict[strings_line[-1]] = [0, len(self.host_list)]
            self.host_list.append(Host(strings_line[-1]))
        elif(device == 'hub'):
            assert(len(strings_line) - 3 == 2), 'Hub should only have name and number of ports'
            self.name_dict[strings_line[-2]] = [1, len(self.hub_list)]
            self.hub_list.append(Hub(strings_line[-2], strings_line[-1]))
        else:
            assert(device == 'host' or device == 'hub'), 'Unknown device'

    def connect_instruction(self, strings_line):
        assert(len(strings_line) - 2 == 2), 'Must have two more arguments'
        first_par = self.name_dict[self.get_device_name(strings_line[2])]
        second_par = self.name_dict[self.get_device_name(strings_line[3])]

        first_device = self.get_device(first_par)
        second_device = self.get_device(second_par)
        first_port = self.get_device_port_index(strings_line[2])
        second_port = self.get_device_port_index(strings_line[3])

        first_device.list_port_connected[first_port - 1] = strings_line[3]
        second_device.list_port_connected[second_port - 1] = strings_line[2]

    def send_instruction(self, strings_line):
        return

    def disconnect_instruction(self, strings_line):
        assert(len(strings_line) - 2 == 1), 'Must have one more argument'
        first_par = self.name_dict[self.get_device_name(strings_line[2])]
        first_device = self.get_device(first_par)
        first_port = self.get_device_port_index(strings_line[2])

        second_par = self.name_dict[self.get_device_name(first_device.list_port_connected[first_port - 1])]
        second_device = self.get_device(second_par)
        second_port = self.get_device_port_index(first_device.list_port_connected[first_port - 1])

    def parse_line(self, line):
        if(len(line) == 0):
            return
        strings_line = line.split(' ')
        time = int(strings_line[0])  #time
        instruction = strings_line[1] #instruction

        if(instruction == 'create'):
           self.create_instruction(strings_line)
        if(instruction == 'connect'):
            self.connect_instruction(strings_line)
        if(instruction == 'disconnect'):
            self.disconnect_instruction(strings_line)

    def execute(self):
        script_file = self.read_file()
        lines_array = script_file.read().split('\n')

        for line in lines_array:
            self.parse_line(line)
        return

protol = MyProtocol('script.txt')
protol.execute()
