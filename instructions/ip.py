from instructions.instruction import Instruction
from network_status import Status
from devices.host import Host
import ip_attribute

class IP(Instruction):
    def __init__(self, input):
        """Init 'ip' instruction information"""

        Instruction.__init__(self,input)

        self.host_name = input[self.start].split(':')
        if(len(self.host_name) > 1):
            self.interface = int(self.host_name[1])
        else:
            self.interface = 1
        self.host_name = self.host_name[0]

        self.ip_address = input[self.start + 1]
        self.mask = input[self.start + 2]

        assert(len(input) == 5), "Instruction ip not valid"

    def execute(self, net_stat : Status):
        device = net_stat.name_index[self.host_name]
        device = net_stat.devices_connect[device]

        device.ip[self.interface - 1].modificate_ip(ip_attribute.IP.ip_normalize(self.ip_address))
        device.ip[self.interface - 1].modificate_mask(ip_attribute.IP.ip_normalize(self.mask))

        ####
        net_stat.ip_mac[self.ip_address] = device