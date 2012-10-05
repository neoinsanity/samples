import sys
from zmq import Context, POLLIN, Poller, SUB, SUBSCRIBE


__author__ = 'neoinsanity'
#
# Weather Client
#

## script contant
# The client will tally the average every five transmissions
avg_sample_size = 5

# each client will only listen for one zip code, and the default is San Jose
zip_filter = sys.argv[1] if len(sys.argv) > 1 else '95128'

# set the initial value of stats collectors
total_temp = 0
recv_count = 0

## setting up the zmq connections
# client socket for message subscription
context = Context()
socket = context.socket(SUB)
socket.connect('tcp://localhost:6668')
socket.setsockopt(SUBSCRIBE, zip_filter)

# socket to receive control messages on
controller = context.socket(SUB)
controller.connect('tcp://localhost:6670')
controller.setsockopt(SUBSCRIBE, "")

# poller for handling receiver and controller messages
poller = Poller()
poller.register(socket, POLLIN)
poller.register(controller, POLLIN)

print 'Collecting updates from weather proxy for zip code: %s ...' % zip_filter
while True:
    socks = dict(poller.poll())

    # exit the program if the kill command is executed
    if socks.get(controller) == POLLIN:
        controller.recv()
        print 'Got kill command'
        break

    if socks.get(socket) == POLLIN:
        string = socket.recv()
        recv_count += 1 # increment the
        print '.',
        zipcode, temperature, relhumidity = string.split()
        total_temp += int(temperature)
        if recv_count == avg_sample_size:
            print "Average temperature for zipcode '%s' was %dF" % (zip_filter, total_temp / avg_sample_size)
            #reset the stats collectors
            totol_temp = 0
            recv_count = 0
