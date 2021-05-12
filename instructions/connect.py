from instructions.instruction import Instruction
from tools import Tools
from network_status import Status
from devices.dev_connected import Dev_connected

class Connect(Instruction):
    def __init__(self, input):
        """Init connect instruction information"""

        Instruction.__init__(self,input)

        self.port1 = input[self.start]
        self.port2 = input[self.start + 1]

        assert(len(input) - 2 == 2), 'Must have two more arguments'

    def execute(self, net_stat : Status):
        first_device_name = Tools.get_device_name(self.port1)
        first_device = net_stat.name_index[first_device_name]
        first_device = net_stat.devices_connect[first_device]
        first_port = Tools.get_device_port_index(self.port1)

        second_device_name = Tools.get_device_name(self.port2)
        second_device = net_stat.name_index[second_device_name]
        second_device = net_stat.devices_connect[second_device]
        second_port = Tools.get_device_port_index(self.port2)

        p1 = first_device.list_port_connected[first_port - 1]
        p2 = second_device.list_port_connected[second_port - 1]

        assert p1 is 'none' or p2 is 'none', 'Port is still connected'

        first_device.list_port_connected[first_port - 1] = self.port2
        second_device.list_port_connected[second_port - 1] = self.port1
