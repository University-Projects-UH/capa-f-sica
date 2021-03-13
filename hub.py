class Hub:
    def __init__(self, name, count_ports):
        self.name = name;
        self.count_ports = int(count_ports);
        self.list_port_connected = []
        for i in range(self.count_ports):
            self.list_port_connected.append('none')
