from host import Host
from hub import Hub
import os

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
        if not '_' in port:
            return 0

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

        try:
            out = open('output/' + strings_line[3] + '.txt','w')
        except:
            os.system('mkdir output')
            out = open('output/' + strings_line[3] + '.txt','w')
        out.close()

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

    def disconnect_instruction(self, strings_line):
        assert(len(strings_line) - 2 == 1), 'Must have one more argument'
        first_par = self.name_dict[self.get_device_name(strings_line[2])]
        first_device = self.get_device(first_par)
        first_port = int(self.get_device_port_index(strings_line[2]))

        second_par = self.name_dict[self.get_device_name(first_device.list_port_connected[first_port - 1])]
        second_device = self.get_device(second_par)
        second_port = int(self.get_device_port_index(first_device.list_port_connected[first_port - 1]))

        first_device.list_port_connected[first_port - 1] = 'none'
        second_device.list_port_connected[second_port - 1] = 'none'


    def send_instruction(self, strings_line):
        assert(len(strings_line) == 4), "Instruction send not valid"

        self.send_list.append(strings_line[2:])

    def parse_line(self, line, time_run):
        if(len(line) == 0):
            return True
        strings_line = line.split(' ')
        time = int(strings_line[0])  #time

        if(time_run < time):
            return False

        instruction = strings_line[1] #instruction

        if(instruction == 'create'):
           self.create_instruction(strings_line)
        elif(instruction == 'connect'):
            self.connect_instruction(strings_line)
        elif(instruction == 'disconnect'):
            self.disconnect_instruction(strings_line)
        elif(instruction == 'send'):
            self.send_instruction(strings_line)

        return True

    def union_name_port(self,name,port):
        return name + '_' + str(port)

    def propagate(self,send_name,bit,i_o,time_act):
        name = self.get_device_name(send_name)
        index = self.get_device_port_index(send_name)
        if(index > 0):
            index -= 1

        device = self.get_device(self.name_dict[name])

        tmp = [self.send_list[0][0],time_act]

        port = self.union_name_port(name,str(index + 1))

        device.read_info[index] = [time_act,port,i_o,bit]
        device.mk_info[index] = tmp

        if(i_o == 'send'):
            connect_device = device.list_port_connected[index]
            tmp1 = self.get_device_name(connect_device)

            if(tmp1 != 'none'):
                tmp2 = self.get_device_port_index(connect_device)
                if(tmp2 > 0):
                    tmp2 -= 1
                connect_device = self.get_device(self.name_dict[tmp1])

                if(connect_device.mk_info[tmp2] != tmp):
                    self.propagate(self.union_name_port(connect_device.name,tmp2 + 1),bit,'receive',time_act)
        elif(i_o == 'receive'):
            for i in range(device.count_ports):
                if(i != index and tmp != device.mk_info[i]):
                    self.propagate(self.union_name_port(device.name,i + 1),bit,'send',time_act)

    def execute(self):
        script_file = self.read_file()
        lines_array = script_file.read().split('\n')

        send_position = 0
        send_time = 0
        self.send_list = []
        time_act = 0
        read_position = 0

        while True:
            if (read_position >= len(lines_array) and len(self.send_list) == 0):
                break

            while read_position < len(lines_array):
                line = lines_array[read_position]

                if not( self.parse_line(line,time_act) ):
                    break

                read_position += 1

            if(len(self.send_list) > 0):
                if(send_time == SIGNAL_TIME):
                    send_position += 1
                    send_time = 0

                if(send_position == len(self.send_list[0][1])):
                    self.send_list = self.send_list[1:]
                    send_position = 0
                    continue

                self.propagate(self.send_list[0][0],self.send_list[0][1][send_position],'send',time_act)

                send_time += 1

            #files output
            for dev in self.host_list:
                out = open('output/' + dev.name + '.txt','a')

                for i in dev.read_info:
                    if(i[0] == 'time' or i[0] < time_act):
                        out.write(str(time_act) + " " + i[1] + ' receive null ')
                    else:
                        for j in i:
                            out.write(str(j) + " ")
                    out.write('ok\n')

            for dev in self.hub_list:
                out = open('output/' + dev.name + '.txt','a')

                for i in dev.read_info:
                    if(i[0] == 'time' or i[0] < time_act):
                        out.write(str(time_act) + " " + i[1] + ' receive null ')
                    else:
                        for j in i:
                            out.write(str(j) + " ")
                    out.write("\n")

            time_act += 1

protol = MyProtocol('script.txt')
protol.execute()
