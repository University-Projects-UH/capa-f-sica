class Mac():
    def __init__(self, _mac = 'none'):
        assert len(_mac) == 4, "Longitud de mac incorrecta"

        self.mac = _mac

    def show(self):
        return self.mac

    def seter(self, new_mac):
        self.mac = new_mac