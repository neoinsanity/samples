from zmq import Context, Poller, POLLIN, PUB, RCVMORE, SNDMORE, SUB, SUBSCRIBE


__author__ = 'neoinsanity'
#
# Weather Proxy
#

context = Context()

# this is the weather server connection
server_sock = context.socket(SUB)
server_sock.connect('tcp://localhost:6667')
server_sock.setsockopt(SUBSCRIBE, "")

# this is public endpoint for subscribers
client_sock = context.socket(PUB)
client_sock.bind("tcp://*:6668")

# socket to receive control messages on
controller = context.socket(SUB)
controller.connect('tcp://localhost:6670')
controller.setsockopt(SUBSCRIBE, "")

# poller for handling receiver and controller messages
poller = Poller()
poller.register(server_sock, POLLIN)
poller.register(controller, POLLIN)

print 'Weather proxy started ...'

# shunt messages out to our own subscriber or handle incomming commandds
while True:
    socks = dict(poller.poll())

    if socks.get(server_sock) == POLLIN:
        # process weather updates to clients
        msg = server_sock.recv()
        more = server_sock.getsockopt(RCVMORE)
        if more:
            client_sock.send(msg, SNDMORE)
        else:
            client_sock.send(msg)

    # any waiting controller command acts as 'KILL'
    if socks.get(controller) == POLLIN:
        controller.recv()
        print 'Got kill command'
        break
