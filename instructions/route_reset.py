from instructions.instruction import Instruction
from network_status import Status

class RouteReset(Instruction):
    def __init__(self, input):
        """Init create instruction information"""

        Instruction.__init__(self,input)

        self.device_name = input[self.start + 1]

    def execute(self, net_stat : Status):
        """Execute route add Instruction"""

        device = net_stat.get_device(self.device_name)

        device.table.reset()
