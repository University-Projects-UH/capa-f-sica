from devices.dev_connected import Dev_connected
from frame import Frame
from tools import Tools
from ip_attribute import IP
from mac_attribute import Mac
from layer_network.frame_special import FrameSpecial
from layer_network.ip_packet import IpPacket

class Host(Dev_connected):
    def __init__(self, info):

        name = info[0]

        Dev_connected.__init__(self,name)

        self.send_collision = 'ok'
        self.receive_collision = 'ok'
        
        self.data = [Frame.empty_frame()] # receive information
        self.verify_info = ''

        self.mac = [Mac()] * self.count_ports
        self.ip = [IP()] * self.count_ports

        open('output/' + self.name + '_data.txt','w')

        self.out_payload = open('output/' + self.name + '_payload.txt','w')
        self.payload = False

        self.signal_count = 0
        
    def is_host(self):
        return True

    def save(self):
        self.data.append(Frame.empty_frame())
        self.verify_data()

        x = self.data[-2]
        if(IpPacket.is_ip_packet(self.data[-2].get_data())):
            self.payload = True

    def stash(self, signal_time):
        if(self.last_receive[0] is 'none'):
            return

        if(self.signal_count == 0):
            frame_act = self.data[-1]

            frame_act.add_bit(self.last_receive[0])

            if(frame_act.length() >= Frame.len_min()):
                if(FrameSpecial.is_special(frame_act.frame)):
                    if(frame_act.length() == 16*2 + 32*2):
                        self.data.append(Frame.empty_frame())
                elif(frame_act.length() == frame_act.len_max()):
                    self.save()
                    
        self.signal_count += 1
        if self.signal_count == signal_time:
            self.signal_count = 0

    def output(self, time):
        out = open('output/' + self.name + '.txt','a')

        for i in range(0,self.count_ports):
            port = self.name + '_' + str(i + 1)

            if(self.last_receive[i] != 'none'):
                out.writelines(str(time) + " " + port + ' receive ' + self.last_receive[i] + ' ' + self.receive_collision + "\n")

            if(self.last_send[i] != 'none'):
                out.writelines(str(time) + " " + port + ' send ' + self.last_send[i] + ' ' + self.send_collision + "\n")
        out.close()

        # frame isn't finished
        if(len(self.data) == 1):
            return 

        frame_out = self.data[-2]

        if not (FrameSpecial.is_special(frame_out.frame)):
            mac = Tools.complete_str_with_char(4,Tools.bin_to_hex(frame_out.get_mac_host()),'0')
            data = Tools.bin_to_hex(frame_out.get_data())

            out = open('output/' + self.name + '_data.txt','a')

            out.writelines(str(time) + " " + mac + " " + data + " " + self.verify_info + "\n")

        if(self.payload):
            frame_data = frame_out.get_data()

            ip_packet_out = IpPacket.str_to_ip_packet(frame_data)

            self.out_payload.write(str(time) + " " + ip_packet_out.get_ip_source_bin() + " " + ip_packet_out.get_data_bin() + "\n")

        self.data.pop(0)
            
    def verify_data(self):
        tmp = self.data[-2]

        if not (tmp.get_verification() == tmp.hash()):
            self.verify_info = 'incorrect'
            return False
        
        self.verify_info = ''
        return True