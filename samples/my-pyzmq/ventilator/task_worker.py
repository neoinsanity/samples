from sys import stdout
import time
from zmq import Context, Poller, POLLIN, PULL, PUSH, SUB, SUBSCRIBE


__author__ = 'neoinsanity'
#
# Task Worker
#

print "Initializing worker ..."

context = Context()

# socket to receive messages on
receiver = context.socket(PULL)
receiver.connect("tcp://localhost:7779")

# socket to send messages to
sender = context.socket(PUSH)
sender.connect("tcp://localhost:7780")

# socket to receive control messages on
controller = context.socket(SUB)
controller.connect("tcp://localhost:6670")
controller.setsockopt(SUBSCRIBE, "")

# poler for handling receiver and controller messages
poller = Poller()
poller.register(receiver, POLLIN)
poller.register(controller, POLLIN)

print "Waiting for job ..."

# poller handling
while True:
    socks = dict(poller.poll())

    if socks.get(receiver) == POLLIN:
        msg = receiver.recv()

        # process task
        workload_msec = int(msg)
        time.sleep(workload_msec * 0.001)

        # send result to sink
        sender.send(msg)

        # progress indicator
        stdout.write('.')
        stdout.flush()

    if socks.get(controller) == POLLIN:
        controller.recv()
        print "Got kill command"
        break
