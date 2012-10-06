from sys import stdout
import time
from zmq import Context, POLLIN, Poller, PULL, SUB, SUBSCRIBE


__author__ = 'neoinsanity'
#
# Task Sink
#


print "Initializing sink ..."

context = Context()

# socket to receive messages on
receiver = context.socket(PULL)
receiver.bind("tcp://*:7780")

# socket for control handling of worker
controller = context.socket(SUB)
controller.connect('tcp://localhost:6670')
controller.setsockopt(SUBSCRIBE, "")

# poller for handling receiver and controller messages
poller = Poller()
poller.register(receiver, POLLIN)
poller.register(controller, POLLIN)

print "Prepared for incoming data ..."

waiting_state = True
tstart = None
recv_count = 0
while True:
    socks = dict(poller.poll())

    if socks.get(receiver) == POLLIN:
        if waiting_state:
            receiver.recv()
            waiting_state = False

            # start our clock now
            tstart = time.time()
            # set the counter
            recv_count = 0

        else:
            recv_count += 1
            receiver.recv()

            if recv_count % 10 == 0:
                stdout.write(':')
            else:
                stdout.write('.')
            stdout.flush()

            if recv_count == 100:
                # calculate and report duration of batch
                tend = time.time()
                tdiff = tend - tstart
                total_msec = tdiff * 1000
                print "Total elapsed time: %d(ms)" % total_msec
                waiting_state = True # go back to waiting for next batch of 100

    # any waiting controller command acts as 'Kill'
    if socks.get(controller) == POLLIN:
        controller.recv()
        break
