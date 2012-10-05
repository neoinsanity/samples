__author__ = 'neoinsanity'
#
# Hello World Client
#

import zmq


context = zmq.Context()

# socket to talk to server
print 'Connecting to hello world server ..."'
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:6666")

# do 10 requests, waiting each time for a response
for request in range(10):
    print "Sending request ", request, "..."
    socket.send("Hello")

    # get the reply
    msg = socket.recv()
    print 'Recieved reply ', request, '[', msg, ']'

