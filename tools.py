
class Tools():
    @classmethod
    def hex_to_bin(self,number):
        return bin(int(number,16))[2:]

    @classmethod
    def bin_to_hex(number):
        return hex(int(number,2))[2:]

    @classmethod
    def complete_str_with_char(self,size,cad,char = '0'):
        return char * int(size - len(cad)) + cad