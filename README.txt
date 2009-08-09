    Gmail push notification proof-of-cocept for iPhone


To be able to use push notifications in your own app you need an
iPhone developer account and a server that has python 2.6 installed.

Steps to run this demo:

 - Create a development notification provisioning profile and sign the
   APNStest app with this profile.  
 - install & run the app on the device
 - note the device token string printed in the debug log
 - exit the app -- no need to run it again.

 - enter the device token in the server/server.py script
 - enter Gmail account credentials into server script
 - create an Apple Push Notification Development certificate
 - export the cert from keychain to cert.p12
 - run:  openssl pkcs12 -in cert.p12 -out certfile.pem -nodes -clcerts

 - start server.py script 

 - send a test email to Gmail
 - the deivce should play an alert sound and display a badge on the
   APNStest app icon indicating the number of unseen emails.


The server script will establish an IMAP connection to Gmail and put
it in IDLE mode. Whenever a new email arrives, Gmail will send a event
notification to our server. The server will query Gmail for the number
of unseen messages and send a notification request to the Apple
server. It requests a sound alert and sets the badge number on the
app's icon to the number of unseen messages.


The server script can easily be extended to send the subject of the
new email to the iPhone and pop up an alert.

This example is based on the following bits of code:


# imaplib2 from: http://www.cs.usyd.edu.au/~piers/python/imaplib2

# example IMAP IDLE server from: http://blog.hokkertjes.nl/2009/03/11/python-imap-idle-with-imaplib2/

# APNS code based on examples from Apple iPhone developer forum postings


 -ge  August 9th, 2009
