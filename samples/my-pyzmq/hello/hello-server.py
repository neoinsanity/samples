__author__ = 'neoinsanity'
#
# Hello World Server
#
import time
import zmq


context = zmq.Context()

# socket to listen to client
responder = zmq.Socket(context, zmq.REP)
responder.bind('tcp://*:6666')

# handle requests
while True:
    request = responder.recv()
    print 'Received request: ', request

    # do some simulated work
    time.sleep(1)

    # send reply
    responder.send('World')


