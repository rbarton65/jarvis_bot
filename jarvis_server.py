'''
    Simple socket server using threads
'''
 
import socket
import sys
import requests
import json
import time
import jarvis
import learn

def parse(data):
	info = data.decode("utf-8").split('\n')[-1]
	result = (json.loads(info))
	print (result)
	jarvis.main(result)
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8001 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
 
#Bind socket to local host and port
try:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print ('Socket bind complete')
 
#Start listening on socket
s.listen(10)
print ('Socket now listening')
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
	conn, addr = s.accept()
	print ('Connected with ' + addr[0] + ':' + str(addr[1]))
	try:
		data = conn.recv(1024)
		parse(data)
	except:
		pass
s.close()
