from devices.dev_connected import Dev_connected
from frame import Frame
from tools import Tools

class Host(Dev_connected):
    def __init__(self, info):

        name = info[0]

        Dev_connected.__init__(self,name)

        self.send_collision = 'ok'
        self.receive_collision = 'ok'
        self.mac = 'none'
        self.data = [Frame.empty_frame()] # receive information
        self.verify_info = ''

        out = open('output/' + self.name + '_data.txt','w')

        self.signal_count = 0
        
    def is_host(self):
        return True

    def stash(self, signal_time):
        if(self.last_receive[0] is 'none'):
            return

        if(self.signal_count == 0):
            frame_act = self.data[-1]

            frame_act.add_bit(self.last_receive[0])

            if(frame_act.length() >= Frame.len_min()):
                if(frame_act.length() == frame_act.len_max()):
                    self.data.append(Frame.empty_frame())
                    self.verify_data()
                    
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

        out = open('output/' + self.name + '_data.txt','a')

        # frame isn't finished
        if(len(self.data) == 1):
            return 

        frame_out = self.data[-2]

        mac = Tools.complete_str_with_char(4,Tools.bin_to_hex(frame_out.get_mac_host()),'0')
        data = Tools.bin_to_hex(frame_out.get_data())

        out.writelines(str(time) + " " + mac + " " + data + " " + self.verify_info + "\n")

        self.data.pop(0)
            
    def verify_data(self):
        tmp = self.data[-2]

        if not (tmp.get_verification() == tmp.hash()):
            self.verify_info = 'incorrect'
            return False
        
        self.verify_info = ''
        return True