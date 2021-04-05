from tools import Tools

class Frame():
    def __init__(self, mac_target, mac_host, data):

        self.frame = Tools.complete_str_with_char(16,Tools.hex_to_bin(mac_target),'0')
        self.frame += Tools.complete_str_with_char(16,Tools.hex_to_bin(mac_host),'0')

        data_size_bin = bin(len(data)//2,)[2:0]
        len_size_bin = len(data_size_bin)

        self.frame += '0' * (8 - len_size_bin) + data_size_bin
        self.frame += '0' * 8
        self.frame += Tools.hex_to_bin(data)

    # def __init__(self, frame):
    #     self.frame = frame

    def add_bit(self, bit):
        self.frame.append(bit)

    def get_mac_target(self):
        return self.frame[0:15]

    def get_mac_host(self):
        return self.frame[16:31]

    def get_data_size(self):
        return self.frame[32,39]

    def get_data(self):
        return self.frame[48:]
    
    def get_extra(self):
        return self.frame[40,47]

