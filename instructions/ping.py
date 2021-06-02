from instructions.instruction import Instruction
from network_status import Status
from instructions.send_packet import SendPacket
from layer_network.ip_packet import IpPacket

class Ping(Instruction):
    def __init__(self, input):
        """Init ping instruction information"""

        Instruction.__init__(self,input)

        self.host_name = input[self.start]
        self.ip_target = input[self.start + 1]

        assert(len(input) == 4), "Instruction ping not valid"

    def execute(self, net_stat : Status):

        echo_request = '08'

        ping = SendPacket(['time','send_packet',self.host_name,self.ip_target,echo_request],protocol='01')

        for i in range(4):
            ping.execute(net_stat)
