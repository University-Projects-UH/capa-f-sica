from protocol import MyProtocol
from exec_status import ExecStatus

protol = MyProtocol('script.txt')

status_actual = ExecStatus(signal_time=5)

# # exectue complete
# while protol.step(status_actual):
#     pass

# execute 'x' miliseconds
x = 999
for i in range(0,x):
    protol.step(status_actual)

#### test

# stat = status_actual.network
# dev_host = 'pc'
# dev_index = stat.name_index[dev_host]
# print(stat.devices_connect[dev_index].list_port_connected[0])
