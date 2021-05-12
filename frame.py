from tools import Tools

BASE = 31
MOD = 10**9+7

class Frame():
    def __init__(self, _mac_target, _mac_host, _data, _verif_size = 8):

        self.verif_size = _verif_size

        self.mac_target = Tools.complete_str_with_char(16,Tools.hex_to_bin(_mac_target),'0')
        self.mac_host = Tools.complete_str_with_char(16,Tools.hex_to_bin(_mac_host),'0')

        if(_data != ''): # data not empty
            self.data = Tools.hex_to_bin(_data)
        else:
            self.data = ''

        self.data_size = Tools.complete_str_with_char(8,self.data,'0')

        self.verif_size_bin = Tools.complete_str_with_char(8,bin(self.verif_size)[2:],'0')
        
        self.frame = self.mac_target + self.mac_host + self.data_size + self.verif_size_bin + self.data
        
        # this line depends last line
        self.frame += self.hash()

    def xor_str(self, cad1, cad2):
        cad1 = Tools.complete_str_with_char(self.verif_size,cad1,'0')
        cad2 = Tools.complete_str_with_char(self.verif_size,cad2,'0')

        r = ''
        for i in range(self.verif_size):
            if(cad1[i] == cad2[i]):
                r += '0'
            else:
                r += '1'

        return r

    def hash(self):
        copy_frame = self.get_mac_target() + self.get_mac_host() + self.get_data_size() + self.get_data() # exclude verification_size

        r = '0' * self.verif_size

        for i in range(0,len(copy_frame),self.verif_size):
            aux = copy_frame[i:i + self.verif_size]

            r = self.xor_str(r,aux)

        return r

    @classmethod
    def str_to_frame(self, str_frame):
        r = Frame('0' * 16,'0' * 16,'')
        r.frame = str_frame

        return r

    @classmethod
    def empty_frame(self):
        r = Frame('0' * 16,'0' * 16,'')
        r.frame = ''

        return r

    @classmethod
    def len_min(self):
        """minimum length"""
        return 48

    def len_max(self):
        """maximum length 'self' frame"""
        return 16 + 16 + 8 + 8 + Tools.bin_to_dec(self.get_data_size()) + Tools.bin_to_dec(self.get_verification_size())

    def get_bit(self, pos):
        return self.frame[pos]

    def length(self):
        return len(self.frame)

    def add_bit(self, bit):
        self.frame += bit

    def get_mac_target(self):
        return self.frame[0:16]

    def get_mac_host(self):
        return self.frame[16:32]

    def get_data_size(self):
        return self.frame[32:40]

    def get_verification_size(self):
        return self.frame[40:48]

    def get_data(self):
        start = 48
        length = Tools.bin_to_dec(self.get_data_size())
        return self.frame[start:start + length]
    
    def get_verification(self):
        start = 48 + Tools.bin_to_dec(self.get_data_size())
        length = Tools.bin_to_dec(self.get_verification_size())
        return self.frame[start:start + length]


