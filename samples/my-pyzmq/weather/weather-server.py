#!/usr/bin/env python
import random
from zipcodes import zip_list
from zmq import Context, Poller, POLLIN, PUB, SUB, SUBSCRIBE

#
# Weather Server
#
if __name__ == '__main__':
    context = Context()
    socket = context.socket(PUB)
    socket.bind('tcp://*:6667')

    # socket to receive control messages on
    controller = context.socket(SUB)
    controller.connect('tcp://localhost:6670')
    controller.setsockopt(SUBSCRIBE, "")

    # poller for handling receiver and controller messages
    poller = Poller()
    poller.register(socket, POLLIN)
    poller.register(controller, POLLIN)

    print 'Weather Update Server started ...'
    while True:
        socks = dict(poller.poll(timeout=1))

        # exit the program if the kill command is executed
        if socks.get(controller) == POLLIN:
            controller.recv()
            print 'Got kill command'
            break

        # if not killed, then tranmit the next weather update
        zipcode = random.choice(zip_list)
        temperature = random.randrange(1, 215) - 80
        relhumidity = random.randrange(1, 50) + 10
        socket.send('%s %d %d' % (zipcode, temperature, relhumidity))
