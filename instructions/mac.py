from instructions.instruction import Instruction
from network_status import Status
from devices.host import Host

class Mac(Instruction):
    def __init__(self, input):
        """Init mac instruction information"""

        Instruction.__init__(self,input)

        self.host_name = input[self.start]
        self.host_mac = input[self.start + 1]

        assert(len(input) == 4), "Instruction mac not valid"

    def execute(self, net_stat : Status):
        device = net_stat.name_index[self.host_name]
        device = net_stat.devices_connect[device]

        device.mac = self.host_mac