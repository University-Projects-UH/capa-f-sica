from tools import Tools
from frame import Frame

class FrameSpecial(Frame):
    ARPQ = '01000001010100100101000001010001'
    ARPQ_HEX = '41525051'
    ARPR = '01000001010100100101000001010010'
    ARPR_HEX = '41525052'

    def __init__(self, _mac_target, _mac_host, _data):

        self.mac_target = Tools.complete_str_with_char(16,Tools.hex_to_bin(_mac_target),'0')
        self.mac_host = Tools.complete_str_with_char(16,Tools.hex_to_bin(_mac_host),'0')

        if(_data != ''): # data not empty
            self.data = Tools.complete_str_with_char(64,Tools.hex_to_bin(_data),'0')
        else:
            self.data = ''

        self.frame = self.mac_target + self.mac_host + self.data

    @classmethod
    def str_to_frame(self, str_frame):
        r = FrameSpecial('0' * 16,'0' * 16,'')
        r.frame = str_frame

        return r

    @classmethod
    def empty_frame(self):
        r = FrameSpecial('0' * 16,'0' * 16,'')
        r.frame = ''

        return r

    @classmethod
    def len_min(self):
        """minimum length"""
        return 16 + 16 + 8 * 8

    def len_max(self):
        """maximum length 'self' frame"""
        return 16 + 16 + 8*8

    def get_mac_target(self):
        return self.frame[0:16]

    def get_mac_host(self):
        return self.frame[16:32]

    def get_data_size(self):
        return ''

    def get_verification_size(self):
        return ''

    def get_data(self):
        return self.frame[32:]
    
    def get_verification(self):
        return ''

    @classmethod
    def is_special(self, frame):
        if(len(frame) < 16*2 + 32):
            return False

        if(frame[32:64] == FrameSpecial.ARPQ or frame[32:64] == FrameSpecial.ARPR):
            return True
        
        return False
