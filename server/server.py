#!/opt/local/bin/python2.6

# example server script that monitors Gmail account via IMAP IDLE and sends 
# push notification to iPhone when new unseen email shows up
#
# imaplib2 from: http://www.cs.usyd.edu.au/~piers/python/imaplib2
# example IMAP IDLE server from: http://blog.hokkertjes.nl/2009/03/11/python-imap-idle-with-imaplib2/
# APNS code based on examples from Apple iPhone developer forum postings
#
# Usage:
#
# create an Apple Push Notification Development certificate
# export the cert from keychain to cert.p12
#   openssl pkcs12 -in certificates.p12 -out certfile.pem -nodes -clcerts
# on device run apns-test and copy the device token string from gdb log
#
# make sure the iPhone app is signed with a provisioning profile that has support for
# development push notifications turned on
#

import socket, ssl, json, struct, re
import imaplib2, time
from threading import *

# enter gmail login details here
USER="YOUR.NAME@gmail.com"
PASSWORD="YOUR-GMAIL-PASSWORD"
# enter device token here
deviceToken = 'XXXXXXXX XXXXXXXX XXXXXXXX XXXXXXXX XXXXXXXX XXXXXXXX XXXXXXXX XXXXXXXX '

currentBadgeNum = -1

def getUnseen():
    (resp, data) = M.status("INBOX", '(UNSEEN)')
    print data
    return int(re.findall("UNSEEN (\d)*\)", data[0])[0])    

def sendPushNotification(badgeNum):
    global currentBadgeNum, deviceToken
    if badgeNum != currentBadgeNum:
        currentBadgeNum = badgeNum
        thePayLoad = {
             'aps': {
        #          'alert':'Hello world!',
                  'sound':'',
                  'badge': badgeNum,
                  },
             'test_data': { 'foo': 'bar' },
             }
        theCertfile = 'certfile.pem'
        theHost = ('gateway.sandbox.push.apple.com', 2195)

        data = json.dumps(thePayLoad)
        deviceToken = deviceToken.replace(' ','').decode('hex')
        theFormat = '!BH32sH%ds' % len(data)
        theNotification = struct.pack(theFormat, 0, 32, deviceToken, len(data), data)

        ssl_sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), certfile=theCertfile)
        ssl_sock.connect(theHost)
        ssl_sock.write(theNotification)
        ssl_sock.close()
        print "Sent Push alert."
 
# This is the threading object that does all the waiting on 
# the event
class Idler(object):
    def __init__(self, conn):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()
 
    def start(self):
        self.thread.start()
 
    def stop(self):
        # This is a neat trick to make thread end. Took me a 
        # while to figure that one out!
        self.event.set()
 
    def join(self):
        self.thread.join()
 
    def idle(self):
        # Starting an unending loop here
        while True:
            # This is part of the trick to make the loop stop 
            # when the stop() command is given
            if self.event.isSet():
                return
            self.needsync = False
            # A callback method that gets called when a new 
            # email arrives. Very basic, but that's good.
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            # Do the actual idle call. This returns immediately, 
            # since it's asynchronous.
            self.M.idle(callback=callback)
            # This waits until the event is set. The event is 
            # set by the callback, when the server 'answers' 
            # the idle call and the callback function gets 
            # called.
            self.event.wait()
            # Because the function sets the needsync variable,
            # this helps escape the loop without doing 
            # anything if the stop() is called. Kinda neat 
            # solution.
            if self.needsync:
                self.event.clear()
                self.dosync()
 
    # The method that gets called when a new email arrives. 
    # Replace it with something better.
    def dosync(self):
        print "Got an event!"
        numUnseen = getUnseen()
        sendPushNotification(numUnseen)

# Had to do this stuff in a try-finally, since some testing 
# went a little wrong.....
#try:
# Set the following two lines to your creds and server
M = imaplib2.IMAP4_SSL("imap.gmail.com")
M.login(USER, PASSWORD)
# We need to get out of the AUTH state, so we just select 
# the INBOX.
M.select("INBOX")
numUnseen = getUnseen()
sendPushNotification(numUnseen)

#print M.status("INBOX", '(UNSEEN)')
# Start the Idler thread
idler = Idler(M)
idler.start()

# Because this is just an example, exit after 8 hours
time.sleep(8*60*60)

#finally:
# Clean up.
idler.stop()
idler.join()
M.close()
# This is important!
M.logout()
