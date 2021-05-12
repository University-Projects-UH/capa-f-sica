from instructions.instruction import Instruction
from devices.host import Host
from devices.hub import Hub
from devices.switch import Switch
from network_status import Status
import os

class Create(Instruction):
    def __init__(self, input):
        """Init create instruction information"""

        Instruction.__init__(self,input)

        self.device = input[self.start]
        self.device_name = input[self.start + 1]
        self.device_info = input[self.start + 1:]

    def execute(self, net_stat : Status):
        """Execute create Instruction"""
        if(self.device == 'host'):
            new_device = Host(self.device_info)
        elif(self.device == 'hub'):
            new_device = Hub(self.device_info)
        elif(self.device == 'switch'):
            new_device = Switch(self.device_info)
        else:
            assert False, 'Unknown device'

        net_stat.name_index[new_device.name] = len(net_stat.devices_connect) # quantity devices connected on network
        net_stat.devices_connect.append(new_device) # add new device on network

