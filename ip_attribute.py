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

    def _convert(self, ip):
        r = ''
        for i in range(0,32,8):
            if(i != 0):
                r += '.'
            r += str(Tools.bin_to_dec(ip[i:i + 8]))

        return r
