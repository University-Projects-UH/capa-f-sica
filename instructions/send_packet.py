from instructions.instruction import Instruction
from network_status import Status
from devices.host import Host
from frame import Frame
from layer_network.frame_special import FrameSpecial
from tools import Tools
from ip_attribute import IP
from layer_network.ip_packet import IpPacket

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

        self.host_mac = device.mac[0].show()

        ### 1st frame (frame_special ARPQ)
        mac_broadcast = 'f' * 4
        mac_source = self.host_mac
        data1 = Tools.complete_str_with_char(8,FrameSpecial.ARPQ_HEX,'0')
        data1 += Tools.complete_str_with_char(8,IP.ip_normalize_hex(self.ip_target),'0')

        frst_frame = FrameSpecial(mac_broadcast,mac_source,data1)

        net_stat.send_wait.append([self.host_name + '_1',frst_frame])

        ### 2nd frame (frame_special ARPR)
        mac_target = mac_source

        dev_target = net_stat.ip_mac[self.ip_target]
        mac_source2 = dev_target.mac[0].show()

        data2 = Tools.complete_str_with_char(8,FrameSpecial.ARPR_HEX,'0')
        data2 += Tools.complete_str_with_char(8,IP.ip_normalize_hex(self.ip_target),'0')

        scnd_frame = FrameSpecial(mac_target,mac_source2,data2)

        net_stat.send_wait.append([dev_target.name + '_1',scnd_frame])

        ### 3rd frame (frame_packet)
        mac_target2 = mac_source2

        mac_source = mac_source

        ip_targ = IP.ip_normalize_hex(self.ip_target)
        ip_targ = Tools.complete_str_with_char(8,ip_targ,'0')

        ip_source = device.ip[0].show_ip()
        ip_source = IP.ip_normalize_hex(ip_source)
        ip_source = Tools.complete_str_with_char(8,ip_source,'0')

        data3 = IpPacket(ip_targ,ip_source,self.data)

        third_frame = Frame(mac_target2,mac_source,data3.packet)
 
        net_stat.send_wait.append([self.host_name + '_1',third_frame])