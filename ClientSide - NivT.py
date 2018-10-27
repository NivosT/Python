#!/usr/bin/python

#NO FUNCTIONS IN SCRIPT

#IMPORTS
from socket import socket, AF_INET, SOCK_STREAM, error
from time import sleep, strftime
from subprocess import Popen, PIPE
import subprocess as sp
from sys import platform

#CHECK PLATFORM, CLOSE IF UNKNOWN
if platform.startswith('linux2'):
    xcut = "/bin/bash"
    plat = "Linux"
    clean = 'clear'
elif platform.startswith('win32'):
    xcut = "c:\Windows\System32\cmd.exe"
    clean = 'cls'
    plat = 'Windows'
else:
    print 'Unknown platform. Not able to run.'
    exit()

#PRINT INTRO
current_time = strftime('%H:%M')
print '''
#############################
# 102 Project | Client Side #
# Made by     | Niv.T       #
# Script must run as root   #
#           %s           #
#############################
Platform: %s
Connection attempt will be made in a few seconds...
[You may hit Ctrl+C at any time to close the program]
'''%(current_time, plat)
sleep(4)
sp.call(clean, shell=True)

#ATTEMPT TO CONNECT TO SERVER
TCP_IP = '127.0.0.1'
TCP_PORT = 5555
BUFFER_SIZE = 4096
s = socket(AF_INET, SOCK_STREAM)
s.settimeout(5)
try:
    s.connect((TCP_IP, TCP_PORT))
    print 'Opening socket to server in port: %s' % (TCP_PORT)
except error as msg:
    print "Socket error: %s" % msg
#INFINITE LOOP OF RECEIVING COMMANDS FROM THE SERVER
try:
    while True:
        try:
            data = s.recv(BUFFER_SIZE)
            if (data == "C"):
                action = s.recv(buffer_size)
                proc = Popen(action, shell=True, stdin=None, stdout=PIPE, stderr=PIPE, executable=xcut)
                out, err = proc.communicate()
            elif (data == "F"):
                des = s.recv(BUFFER_SIZE)
                f = open(des, 'wb')
                while True:
                    try:
                        data = s.recv(1024)
                        if data == "E":
                            f.close()
                            break
                        f.write(data)
                    except:
                        f.close()
                        break
            elif (data == "P"):
                pack_info = s.recv(BUFFER_SIZE)
                proc = Popen(pack_info, shell=True, stdin=None, stderr=None, executable=xcut)
                proc.wait()
            else:
                proc = Popen(data, shell=True, stdin=None, stdout=PIPE, stderr=PIPE, executable=xcut)
                out, err = proc.communicate()
                if (out == ""):
                    s.send(err)
                else:
                    s.send(out)
        except Exception as e:
            continue

except KeyboardInterrupt:
    print '\nYou chose to exit the program.\nGoodbye.\n[Closing the connection]'
    exit()


s.close()
