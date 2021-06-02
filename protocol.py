from network_status import Status
from parse import Parse
from instructions.instruction import Instruction

class MyProtocol():
    def __init__(self, filename):
        self.filename = filename
        script_file = open(self.filename, 'r') # Read script.txt
        self.lines_array = script_file.read().split('\n') # Separate per lines

    def step(self, stat):

        # Read and execute instruction
        while stat.read_position < len(self.lines_array):
            line = self.lines_array[stat.read_position]
            inst = Parse.line(line, stat.time_act)

            if not inst:
                break
            stat.read_position += 1

            if inst == True:
                continue
            
            inst.execute(stat.network)

        finish_read = stat.read_position >= len(self.lines_array)

        status_send = stat.network.send() # True if send something, False otherway
        stat.network.output(stat.time_act)

        stat.time_act += 1

        if(status_send or (not finish_read)):
            return True
        return False
