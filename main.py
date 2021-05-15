from protocol import MyProtocol
from exec_status import ExecStatus
import os

protol = MyProtocol('script.txt')

status_actual = ExecStatus(signal_time=10)

# exectue complete
while protol.step(status_actual):
    pass

# execute 'x' miliseconds
# x = 900
# for i in range(0,x):
#     protol.step(status_actual)


# ### test
# import asserts