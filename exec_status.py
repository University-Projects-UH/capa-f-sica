from network_status import Status

class ExecStatus:
    def __init__(self, signal_time = 10):
        self.time_act = 0
        self.read_position = 0
        self.network = Status(signal_time)
