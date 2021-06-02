from tools import Tools
from ip_attribute import IP

class IpPacket():
    def __init__(self, ip_target, ip_source, data, ttl = '00',protocol = '00'):
        """Info is on hexadecimal"""
        self._ip_target = ip_target
        self._ip_source = ip_source

        self._ttl = ttl
        self._protocol = protocol

        self._data = data
        self._payload_size = Tools.complete_str_with_char(2,hex(len(data))[2:],'0')

        self.packet = ip_target + ip_source + ttl + protocol + self._payload_size + data

    @classmethod
    def is_ip_packet(self, data):
        if(len(data) < 88):
            return False
        tmp_payload_size = Tools.bin_to_dec(data[80:88])

        if(len(data) == 88 + tmp_payload_size*4):
            return True
        return False

    @classmethod
    def str_to_ip_packet(self, _str):
        new_ip_packet = IpPacket('00000000','00000000','')

        new_ip_packet.packet = _str

        return new_ip_packet

    def get_ip_source_bin(self):
        return IP.ip_standardize(self.packet[32:64])

    def get_data_bin(self):
        return Tools.bin_to_hex(self.packet[88:])