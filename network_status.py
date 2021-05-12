from frame import Frame
from queue import Queue
from tools import Tools
from devices.host import Host

class Status:
    def __init__(self, signal_time = 10):
        self.signal_time = signal_time
        self.signal_count = 0

        self.devices_connect = []   # dev_connect array
        self.name_index = {}        # dictionary[name_device] -> index(devices_connect)

        self.send_list = []         # frame sending
        self.send_pos_frame = []    # sending position

        self.send_wait = []         # waiting frame to send

    def get_device(self, name):
        ind = self.name_index[name]
        return self.devices_connect[ind]

    def send(self):
        """send only one frame once time (don't have collision)"""
        send_pos = 0 

        # send list not empty
        if(len(self.send_list) == 0): 
            if(len(self.send_wait) == 0):
                return False
            self.send_list.append(self.send_wait[0])    # add send list
            self.send_pos_frame.append(0)
            self.send_wait.pop(0)                       # refresh send_wait

        send_now = self.send_list[send_pos]
        host = send_now[0] # port send frame
        frame = send_now[1]  

        bit = frame.get_bit(self.send_pos_frame[send_pos])

        q = Queue()

        q.put((host,'s'))
 
        # 's': send, 'r': receive
        while not q.empty():
            front = q.get()
            name_port = front[0]
            tp = front[1] # type operation: 'r' o 's'

            name = Tools.get_device_name(name_port)
            port = Tools.get_device_port_index(name_port)

            dev = self.get_device(name)
            
            if(tp == 's'):
                new_dev = dev.send(bit, port)
            else: # tp == 'r'
                new_dev = dev.receive(bit, port)
                
            for i in new_dev:
                q.put(i)

        # signal time
        self.signal_count += 1
        if(self.signal_count == self.signal_time):
            self.send_pos_frame[send_pos] += 1
            if(self.send_pos_frame[send_pos] == frame.length()): # if frame send complete
                #reset send list
                self.send_list.pop(send_pos)
                self.send_pos_frame.pop(send_pos)

            self.signal_count = 0
        
    def output(self, time):
        for dev in self.devices_connect:
            dev.stash(self.signal_time) # save changes
            dev.output(time)            # print information
            dev.clean()                 # reset 
            

