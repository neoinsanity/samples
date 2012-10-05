import time
from zmq import Context, PUB


__author__ = 'neoinsanity'
#
# Kill Signaller
#

print "Sending kill signal ..."

context = Context()

# socket for worker control
controller = context.socket(PUB)
controller.bind('tcp://*:6670')

# give a little time to ensure that the bind occurs
time.sleep(1)

# send the kill command
controller.send("KILL")

# give it time for zmq to send signal
time.sleep(1)

