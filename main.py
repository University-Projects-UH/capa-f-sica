from host import Host
from hub import Hub
from frame import Frame
from tools import Tools
from switch import Switch
import os

SIGNAL_TIME = 1

class MyProtocol():
    def __init__(self, filename):
        self.filename = filename
        self.host_list = []
        self.hub_list = []
        self.switch_list = []
        self.name_dict = {}
        ###
        self.dic = {'pc' : '', 'pc2' : ''}

    def ignore_comments(self, line):
        new_line = ''
        for c in line:
            if(c == '#'):
                break
            new_line += c
        return new_line

    def my_split_by_spaces(self, line):
        argum = ''
        line_splited = []
        for c in line:
            if(c == ' '):
                if(len(argum) > 0):
                    line_splited.append(argum)
                argum = ''
                continue
            argum += c
        if(len(argum) > 0):
            line_splited.append(argum)
        return line_splited

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
        elif(par[0] == 1):
            return self.hub_list[par[1]] #is a hub
        return self.switch_list[par[1]] #is a switch

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
        elif(device == 'switch'):
            assert(len(strings_line) - 3 == 2), 'Switch should only have name and number of ports'
            self.name_dict[strings_line[-2]] = [2, len(self.switch_list)]
            self.switch_list.append(Switch(strings_line[-2], strings_line[-1]))
        else:
            assert False, 'Unknown device'

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

        

    def mac_instruction(self, strings_line):
        assert(len(strings_line) == 4), "Instruction mac not valid"

        par = self.name_dict[self.get_device_name(strings_line[2])]
        device = self.get_device(par)

        device.mac = strings_line[3]

    def send_frame_instruction(self, strings_line):
        #strings_line: host_name, mac_target, data
        host_name = strings_line[-3]
        mac_target = strings_line[-2]
        data = strings_line[-1]

        mac_host = self.name_dict[self.get_device_name(host_name)]
        mac_host = self.get_device(mac_host)
        mac_host = mac_host.mac

        new_frame = Frame(mac_target, mac_host, data)

        self.send_list.append([host_name,new_frame])

    def send_instruction(self, strings_line):
        assert(len(strings_line) == 4), "Instruction send not valid"

        #send address(all host)
        mac = 'FFFF'

        #convert binary to hexadecimal
        data_hex = hex(int('0b' + strings_line[-1],2))

        #pop back
        strings_line.pop()

        strings_line += [mac,data_hex]

        self.send_frame_instruction(strings_line)

    def parse_line(self, line_, time_run):
        line = self.ignore_comments(line_)
        if(len(line) == 0):
            return True
        strings_line = self.my_split_by_spaces(line)
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
        elif(instruction == 'mac'):
            self.mac_instruction(strings_line)
        elif(instruction == 'send_frame'):
            self.send_frame_instruction(strings_line)

        return True

    def union_name_port(self,name,port):
        return name + '_' + str(port)

    def propagate(self,send_name,bit,i_o,time_act,end_frame):
        name = self.get_device_name(send_name)
        index = self.get_device_port_index(send_name)
        if(index > 0):
            index -= 1

        device = self.get_device(self.name_dict[name])

#errrrrrrooooooooooorrrr
        tmp = [self.send_list[0][0],time_act]

        port = self.union_name_port(name,str(index + 1))

        if(i_o == 'send'):
            #mark 
            device.send_info[index] = [time_act,port,i_o,bit]
            device.send_mk_info[index] = tmp

            connect_device = device.list_port_connected[index]
            tmp1 = self.get_device_name(connect_device)

            if(tmp1 != 'none'):
                tmp2 = self.get_device_port_index(connect_device)
                if(tmp2 > 0):
                    tmp2 -= 1
                connect_device = self.get_device(self.name_dict[tmp1])

                if(connect_device.read_mk_info[tmp2] != tmp):
                    if(connect_device.read_mk_info[tmp2][1] == time_act):
                        return False
                    if self.propagate(self.union_name_port(connect_device.name,tmp2 + 1),bit,'receive',time_act,end_frame) == False:
                        return False
        elif(i_o == 'receive'):
            #mark 
            device.read_info[index] = [time_act,port,i_o,bit]
            device.read_mk_info[index] = tmp

            for i in range(device.count_ports):
                if(i != index and tmp != device.send_mk_info[i]):
                    if(device.send_mk_info[i][1] == time_act):
                        return False

                    if self.propagate(self.union_name_port(device.name,i + 1),bit,'send',time_act,end_frame) == False:
                        return False

            #write information
            if(device.is_host()):
                device.data[-1] += bit
                # self.dic[device.name] += bit
                if(end_frame):
                    data_tmp = device.data[-1]
                    device.data[-1] = [time_act,data_tmp[16:32],data_tmp]
                    device.data.append('')


        return True

    def execute(self):
        script_file = open(self.filename, 'r') # Read script.txt
        lines_array = script_file.read().split('\n') # Separate per lines

        send_position = [0]
        send_time = [0]
        self.send_list = []
        time_act = 0
        read_position = 0

        while True:
            #EOF read file and End send list
            if (read_position >= len(lines_array) and len(self.send_list) == 0):
                break

            while read_position < len(lines_array):
                line = lines_array[read_position]

                if not( self.parse_line(line,time_act) ):
                    break

                read_position += 1

            wait_for_remove = []

            for i in range(len(self.send_list)):
                if(len(send_position) == i):
                    send_position.append(0)
                    send_time.append(0)

                #propagate information to the network
                send_name = self.send_list[i][0]
                bit = self.send_list[i][1].frame[send_position[i]]
                end_frame = send_position[i] + 1 == len(self.send_list[i][1].frame)
                # self.dic[send_name] += bit
                # if(end_frame):
                #     print(time_act, self.dic[send_name])
                if(self.propagate(send_name,bit,'send',time_act,end_frame) == False):
                    break

                send_time[i] += 1

                if(send_time[i] == SIGNAL_TIME):
                    send_position[i] += 1
                    send_time[i] = 0

                if(send_position[i] >= len(self.send_list[i][1].frame)):
                    wait_for_remove.append(i)

### errrrrrrrrooooooooorrrrrrrr
            for i in wait_for_remove:
                self.send_list.pop(i)
                send_position.pop(i)
                send_time.pop(i)

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

                for i in dev.send_info:
                    if(i[0] == 'time' or i[0] < time_act):
                        out.write(str(time_act) + " " + i[1] + ' send null ')
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

                for i in dev.send_info:
                    if(i[0] == 'time' or i[0] < time_act):
                        out.write(str(time_act) + " " + i[1] + ' sends null ')
                    else:
                        for j in i:
                            out.write(str(j) + " ")
                    out.write("\n")

            for dev in self.switch_list:
                out = open('output/' + dev.name + '.txt','a')

                for i in dev.read_info:
                    if(i[0] == 'time' or i[0] < time_act):
                        out.write(str(time_act) + " " + i[1] + ' receive null ')
                    else:
                        for j in i:
                            out.write(str(j) + " ")
                    out.write("\n")

                for i in dev.send_info:
                    if(i[0] == 'time' or i[0] < time_act):
                        out.write(str(time_act) + " " + i[1] + ' send null ')
                    else:
                        for j in i:
                            out.write(str(j) + " ")
                    out.write("\n")

            time_act += 1

        #output data_hosts
        for dev in self.host_list:
            out = open('output/' + dev.name + '_data.txt','w')

            for i in dev.data:
                out.write(str(i) + " ")
            out.write("\n")

        for i in self.dic:
            print(i,self.dic[i])

protol = MyProtocol('script.txt')
protol.execute()
