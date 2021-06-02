
class Tools():
    
    @classmethod # static method
    def hex_to_bin(self,number):
        return bin(int(number,16))[2:]

    @classmethod
    def bin_to_hex(self,number):
        return hex(int(number,2))[2:]

    @classmethod
    def bin_to_dec(self,number):
        return int(number,2)

    @classmethod
    def complete_str_with_char(self,size,cad,char = '0'):
        return char * int(size - len(cad)) + cad

    @classmethod
    def get_device_name(self, port):
        name = ''
        for c in port:
            if(c == '_'):
                break
            name += c

        return name

    @classmethod
    def get_device_port_index(self, port):
        """Return number port, give one port"""
        if not '_' in port:
            return 1

        port_index = ''
        len_port = len(port)
        for i in range(len(port)):
            if(port[len_port - i - 1] == '_'):
                break
            port_index += port[len_port - i - 1]

        return int(port_index[::-1])

    @classmethod
    def union_name_port(self,name,port):
        return name + '_' + str(port)

    @classmethod
    def and_strings(self, cad1, cad2, length):
        c1 = Tools.complete_str_with_char(length,cad1,'0')
        c2 = Tools.complete_str_with_char(length,cad2,'0')

        r = ""
        for i in range(len):
            if(c1[i] == c2[i]):
                r += c1[i]
            else:
                r += '0'

        return r