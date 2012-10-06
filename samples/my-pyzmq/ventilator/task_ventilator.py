import random
import time
from zmq import Context, PUSH


__author__ = 'neoinsanity'
#
# Task Ventilator
#

context = Context()

# socket to send messages on
sender = context.socket(PUSH)
sender.bind("tcp://*:7779")

# socket with direct access to the sink: used to synchronize start of batch
sink = context.socket(PUSH)
sink.connect("tcp://localhost:7780")

_ = raw_input('Press Enter when workers are ready: ')
print "Sending tasks to workers ...."

# the first message is "0" and signals start of batch
sink.send('0')

# initialize random number generator
random.seed()

# send 100 tasks
total_sec = 0
for task_nbr in range(100):
    # random workload from 1 to 100 milliseconds
    workload = random.randint(1, 100)
    total_sec += workload

    sender.send(str(workload))

print "Total expected cost: %s(msec)" % total_sec

# give 0mq time to deliver the messages
time.sleep(1)
