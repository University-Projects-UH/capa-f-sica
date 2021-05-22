from instructions.instruction import Instruction

from instructions.create import Create
from instructions.connect import Connect
from instructions.disconnect import Disconnect
from instructions.mac import Mac
from instructions.send import Send
from instructions.send_frame import SendFrame
from instructions.ip import IP
from instructions.send_packet import SendPacket
from instructions.route_add import RouteAdd
from instructions.route_delete import RouteDelete
from instructions.route_reset import RouteReset

from instructions.ping import Ping

class Parse:

    @classmethod
    def line(self, line_, time_run):
        """Parse one instruction line, return one object type instruction"""
        line = self.ignore_comments(self,line_)
        if(len(line) == 0):
            return True

        strings_line = self.my_split_by_spaces(self,line)
        time = int(strings_line[0])  #time

        if(time_run < time):
            return False

        instruction = strings_line[1] #instruction

        if(instruction == 'create'):
            inst = Create(strings_line)
        elif(instruction == 'connect'):
            inst = Connect(strings_line)
        elif(instruction == 'disconnect'):
            inst = Disconnect(strings_line)
        elif(instruction == 'mac'):
            inst = Mac(strings_line)
        elif(instruction == 'send'):
            inst = Send(strings_line)
        elif(instruction == 'send_frame'):
            inst = SendFrame(strings_line)
        elif(instruction == 'ip'):
            inst = IP(strings_line)
        elif(instruction == 'send_packet'):
            inst = SendPacket(strings_line)
        elif(instruction == 'route'):
            instruction2 = strings_line[2]
            if(instruction2 == 'add'):
                inst = RouteAdd(strings_line)
            elif(instruction2 == 'delete'):
                inst = RouteDelete(strings_line)
            elif(instruction2 == 'reset'):
                inst = RouteReset(strings_line)
        elif(instruction == 'ping'):
            inst = Ping(strings_line)

        return inst

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
