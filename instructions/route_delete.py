from instructions.instruction import Instruction
from network_status import Status
from layer_network.route import Route

class RouteDelete(Instruction):
    def __init__(self, input):
        """Init create instruction information"""

        Instruction.__init__(self,input)

        self.device_name = input[self.start + 1]
        self.destination = input[self.start + 2]
        self.mask = input[self.start + 3]
        self.gateway = input[self.start + 4]
        self.interface = input[self.start + 5]

    def execute(self, net_stat : Status):
        """Execute route delete Instruction"""

        device = net_stat.get_device(self.device_name)

        route_act = Route(self.destination,self.mask,self.gateway,self.interface)

        device.table.delete(route_act)
