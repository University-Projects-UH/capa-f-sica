from instructions.instruction import Instruction
from tools import Tools
from network_status import Status
from devices.dev_connected import Dev_connected

class Disconnect(Instruction):
    def __init__(self, input):
        """Init disconnect instruction information"""

        Instruction.__init__(self,input)

        self.port = input[self.start]

        assert(len(input) - 2 == 1), 'Instruction disconnect must have one more argument'

    def execute(self, net_stat : Status):
        first_device_name = Tools.get_device_name(self.port)
        first_device = net_stat.name_index[first_device_name]
        first_device = net_stat.devices_connect[first_device]
        first_port = Tools.get_device_port_index(self.port)

        p1 = first_device.list_port_connected[first_port - 1]

        # port is not connect on network
        if(p1 is 'none'):
            return

        second_device_name = Tools.get_device_name(p1)
        second_device = net_stat.name_index[second_device_name]
        second_device = net_stat.devices_connect[second_device]
        second_port = Tools.get_device_port_index(p1)

        first_device.list_port_connected[first_port - 1] = 'none'
        second_device.list_port_connected[second_port - 1] = 'none'

        # do something(connection error, etc)