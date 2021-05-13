from instructions.instruction import Instruction
from network_status import Status
from devices.host import Host
from frame import Frame

class SendPacket(Instruction):
    def __init__(self, input):
        """Init send packet instruction information"""

        Instruction.__init__(self,input)

        self.host_name = input[self.start]
        self.ip_target = input[self.start + 1]
        self.data = input[self.start + 2]

        assert(len(input) == 5), "Instruction send packet not valid"

    def execute(self, net_stat : Status):
        device = net_stat.name_index[self.host_name]
        device = net_stat.devices_connect[device]

        self.host_mac = device.mac

        new_frame = Frame(self.mac_target,self.host_mac,self.data)

        net_stat.send_wait.append([self.host_name + '_1',new_frame])