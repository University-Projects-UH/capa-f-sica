from instructions.instruction import Instruction
from network_status import Status
from instructions.send_frame import SendFrame
from tools import Tools

class Send(Instruction):
    def __init__(self, input):
        """Init send instruction information"""

        Instruction.__init__(self,input)

        self.host_name = input[self.start]

        self.mac_target = 'FFFF'

        self.data = input[self.start + 1]
        self.data = Tools.bin_to_hex(self.data)

        assert(len(input) == 4), "Instruction send not valid"

    def execute(self, net_stat : Status):
        send = SendFrame(['time','send_frame',self.host_name,self.mac_target,self.data])

        send.execute(net_stat)