
import sys
from ex2utils import Client

import time

# TASK 2.6
class IRCClient(Client):

    def onMessage(self, socket, message):
        if (message[0] == "!"):
            print(message[1:])
        else:
            print(message)
            print("\n> Enter a command:")
        return True


# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])
screenName = sys.argv[3]

# Create an IRC client.
client = IRCClient()

# Start server
client.start(ip, port)

print("\nCommands are as follows:\nNAME username - set your username\nMESSAGEALL message- to message all online users\nMESSAGE username message - message a select user\nLIST - lists all online users\nEXIT - leave session\n\nTo choose a command and enter a message type for example: 'ALL hello everyone, how are we'\n")

# *** register your client here, e.g. ***
message = "NAME " + screenName
client.send(message.encode())

while client.isRunning():
    command = input()
    if (command == "EXIT"):
        command = command.encode()
        client.send(command)
        client.stop()
        print("Closing the connection . . .")
        print("Connection closed")
    else:
        command = command.encode()
        client.send(command)
        print("\n> Enter a command:")
    
client.stop()
