from devices.hub import Hub

class Switch(Hub):
    def __init__(self, info):

        Hub.__init__(self, info)
        # mac_table <key, value>, key is the destination host's mac, and value is the port
        # where the information should be sent
        mac_table = {}
