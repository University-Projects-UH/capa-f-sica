from host import Host;
from hub import Hub;

SIGNAL_TIME = 10;

class MyProtocol():
    def __init__(self, filename):
        self.filename = filename;
        self.host_list = [];
        self.hub_list = [];
        return;

    def read_file(self):
        return open(self.filename, 'r'); #Read script.txt

    def parse_line(self, line):
        if(len(line) == 0):
            return;
        strings_line = line.split(' ');
        time = int(strings_line[0]);  #time
        instruction = strings_line[1]; #instruction

        if(instruction == 'create'):
            device = strings_line[2];
            if(device == 'host'):
                assert(len(strings_line) - 3 == 1), 'Host should only have name';
                self.host_list.append(Host(strings_line[-1]));
            elif(device == 'hub'):
                self.hub_list.append(Hub(strings_line[-2], strings_line[-1]));
                assert(len(strings_line) - 3 == 2), 'Hub should only have name and number of ports';
            else:
                assert(device == 'host' or device == 'hub'), 'Unknown device';

    def execute(self):
        script_file = self.read_file();
        lines_array = script_file.read().split('\n');

        for line in lines_array:
            self.parse_line(line);
        return;

protol = MyProtocol('script.txt');
protol.execute();
