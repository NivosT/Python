#!/usr/bin/python

####   \/\/ START FROM MAIN FUNCTION \/\/

from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, error
import socket
from thread import start_new_thread
from time import sleep, strftime
from sys import platform
import subprocess as sp
from os import kill, getpid

#SOCKET CREATION
try:
    s = socket.socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    host = ''
    port = 5555
    BUFFER_SIZE = 4096
    s.bind((host, port))
    connections = []
    max_connections = 5
    s.listen(max_connections)
except error as msg:
    print "Socket Error: %s" % msg
    exit()

#GET CLIENTS CONNECTED TO THE SERVER
def GetConnections():
    if len(connections)==0:
        print 'No Clients are connected to the server!\nUnable to continue with the request.'
        Back()
    else:
        print 'Clients connected to the server:'
        num = 1
        for client in connections:
            ip = client[1][0]
            print "[%s] ip %s" % (num, ip)
            num += 1

#~THE NEXT 6 FUNCTIONS ARE ACTIONS REFERRED FROM THE MENU~
def ShowClients():
    blank()
    GetConnections()
    Back()

def Command_send():
    blank()
    print '''
    ~~Command sending option~~
    '''
    GetConnections()
    inp = int(raw_input("Enter Client Number or 0 for all "))
    com = raw_input("Enter command to send: ")

    if inp == 0:
        for i in connections:
            try:
                i[0].send('C')
                i[0].send(com)
                print(i[1], " success")
                sleep(1)
                print(i[0].recv(BUFFER_SIZE))
            except:
                print(i[1], " failed")
                connections.remove(i)
                break
    else:
        try:
            connections[inp - 1][0].send('C')
            connections[inp - 1][0].send(com)
            print(connections[inp - 1][1], " success")
            print(connections[inp - 1][0].recv(BUFFER_SIZE))
        except:
            print(connections[inp - 1][1], " failed")
            connections.remove(connections[inp - 1])
            return

def transfer():
    blank()
    print '''
        ~~File transfer option~~
        '''
    GetConnections()
    inp = int(raw_input("Enter Client Number or 0 for all "))
    sourcefile = raw_input("Enter file source (full path):")
    destination = raw_input("Enter file destination (full path):")
    if inp == 0:
        for i in connections:
            try:
                i[0].send("F")

                print(i[1], " success")
            except:
                print(i[1], " failed")
                connections.remove(i)
                break
            sleep(1)
            i[0].send(destination)
            f = open(sourcefile, 'rb')
            l = f.read(1024)
            while (l):
                i[0].send(l)
                l = f.read(1024)
            f.close()
            i[0].send("E")
    else:
        try:
            connections[inp - 1][0].send("F")
            print(connections[inp - 1][1], "success")
        except:
            print(connections[inp - 1][1], " failed")
            connections.remove(connections[inp - 1])
            return
        sleep(1)
        connections[inp - 1][0].send(destination)
        f = open(sourcefile, 'rb')
        l = f.read(1024)
        while (l):
            connections[inp - 1][0].send(l)
            l = f.read(1024)
        f.close()
        sleep(1)
        connections[inp - 1][0].send("E")
    Back()


def install():
    blank()
    print '''
        ~~Installing option~~
        '''
    GetConnections()
    inp = int(raw_input("Enter Client Number or 0 for all "))
    program = raw_input("Enter Source Program ")
    InstallApp = "apt-get -y install %s" % (program)
    if inp == 0:
        for i in connections:
            try:
                i[0].send("P")
                print(i[1], " success")
            except:
                print(i[1], " failed")
                connections.remove(i)
                break
            sleep(1)
            i[0].send(InstallApp)
    else:
        try:
            connections[inp - 1][0].send("P")
            print(connections[inp - 1][1], " success")
        except:
            print(connections[inp - 1][1], " failed")
            connections.remove(connections[inp - 1])
            return
        connections[inp - 1][0].send(InstallApp)
    Back()

def remove():
    blank()
    print '''
        ~~Removing option~~
        '''
    GetConnections()
    inp = int(raw_input("Enter Client Number or 0 for all "))
    program = raw_input("Enter Source Program ")
    RemoveApp = "apt-get -y remove %s" % (program)
    if inp == 0:
        for i in connections:
            try:
                i[0].send("P")
                print(i[1], " success")
            except:
                print(i[1], " failed")
                connections.remove(i)
                break
            sleep(1)
            i[0].send(RemoveApp)
    else:
        try:
            connections[inp - 1][0].send("P")
            print(connections[inp - 1][1], " success")
        except:
            print(connections[inp - 1][1], " failed")
            connections.remove(connections[inp - 1])
            return
        sleep(1)
        connections[inp - 1][0].send(RemoveApp)
    Back()

def out():
    blank()
    print 'You chose to exit the program. Goodbye.'
    kill((getpid()), 9)

#FUNCTION FOR WRONG INPUT IN DICT
def wrong():
    print "Wrong input.\n[Hit enter to try again]"
    raw_input()
    blank()
    menu(a=1)


#FUNCTION TO CLEAR THE SCREEN ACCORDING TO PLATFORM
def blank():
    sp.call(clean, shell=True)
#FUNCTION TO RETURN TO MENU
def Back():
    print '[Hit enter to return to the menu]'
    raw_input()
    blank()
    menu(a=1)

#CHECK THE PLATFORM, CLOSE IF NOT LINUX/WIN
def PostIntro():
    global clean
    global plat
    if platform.startswith('linux2'):
        plat = "Linux"
        clean = 'clear'

    elif platform.startswith('win32'):
        clean = 'cls'
        plat = 'Windows'

    else:
        print 'Unknown platform. Not able to run.'
        exit()

#INTRO TO THE PROJECT, RUNS ONLY AT THE BEGINNING
def intro():
    current_time = strftime("%H:%M")
    print '''
    #############################
    # 102 Project | Server Side #
    # Made by     | Niv.T       #
    # Script must run as root   #
    #           %s           #
    #############################
    Platform: %s
    Socket port: %s

    '''%(current_time, plat, port)

#OPTIONS FOR SERVER
def menu(a):
    print """
    Available action to take:
    [1] Show all clients
    [2] Send commands to all clients
    [3] Transfer file to all clients
    [4] Install something on all clients
    [5] Remove something from all clients
    [6] Exit the program
    """
    choice = raw_input('choose an option from the list [+]: \n ')


#REFERS TO FUNCTIONS TO COMPLETE REQUEST ^^

    dict = {
        "1": ShowClients,
        "2": Command_send,
        "3": transfer,
        "4": install,
        "5": remove,
        "6": out
        }

    print dict.get(choice, wrong)()


#START HERE
#SENDS TO INTRO FUNCTIONS
def main():
    PostIntro()
    intro()

main()
start_new_thread(menu, (1,)) #THREADING, RUNS THE MENU

#CONNECTION LOOP
while True:
    conn, addr = s.accept()
    connections.append([conn, addr])
s.close()

