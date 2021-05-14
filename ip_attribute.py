from tools import Tools

class IP():
    def __init__(self, _ip = 'none', _mask = 'none'):
        self.mask = _mask
        self.ip = _ip

    def show_ip(self):
        return self._convert(self.ip)
    
    def modificate_ip(self, new_ip):
        self._validate(new_ip)

        self.ip = new_ip

    def show_mask(self):
        return self._convert(self.mask)
        
    def modificate_mask(self, new_mask):
        self._validate(new_mask)

        self.mask = new_mask

    def _validate(self, ip):
        assert len(ip) == 32, "Longitud de IP incorrecta"

    @classmethod
    def ip_standardize(self, ip_bin):
        """convert 11111111111111110000000000000000(normal) to 255.255.0.0(standard)"""
        r = ''
        for i in range(0,32,8):
            if(i != 0):
                r += '.'
            r += str(Tools.bin_to_dec(ip_bin[i:i + 8]))

        return r        

    @classmethod
    def ip_standardize_hex(self, ip_hex):
        """convert ffff0000(normal) to 255.255.0.0(standard)"""
        info_bin = Tools.complete_str_with_char(32,Tools.hex_to_bin(ip_hex),'0')

        return self.ip_standardize(info_bin)

    @classmethod
    def ip_normalize(self, ip_standard):
        """convert 255.255.0.0(standard) to 11111111111111110000000000000000(normal)"""
        tmp = ip_standard.split('.')
        r = ''
        for i in range(len(tmp)):
            byte = bin(int(tmp[i]))[2:]
            byte = Tools.complete_str_with_char(8,byte,'0')
            r += byte

        return r

    @classmethod
    def ip_normalize_hex(self, ip_standard):
        """convert 255.255.0.0(standard) to ffff0000(normal)"""
        r = self.ip_normalize(ip_standard)
        r = Tools.bin_to_hex(r)

        return r

    def _convert(self, ip):
        r = ''
        for i in range(0,32,8):
            if(i != 0):
                r += '.'
            r += str(Tools.bin_to_dec(ip[i:i + 8]))

        return r
