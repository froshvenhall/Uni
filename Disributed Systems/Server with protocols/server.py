from os import times
import sys
from ex2utils import Server

class MyServer(Server):
    global noUsers
    noUsers = 0
    global users
    users = []

    def onStart(self):
        print("MyServer has started")

    def onStop(self):
        print("Shutting down")
    
    def onConnect(self, socket):
        # TASK 2.1
        global noUsers
        noUsers += 1
        global users
        users.append(socket)

        # TASK 2.2
        print("Live users = ", noUsers)
        print("New user connected")

    def onMessage(self, socket, message):
        # This function takes two arguments: 'socket' and 'message'.
        #     'socket' can be used to send a message string back over the wire.
        #     'message' holds the incoming message string (minus the line-return).

        # convert the string to an upper case version

        # TASK 2.1
        (command, sep, parameter) = message.strip().partition(' ')
        print("Command is ", command)

        # TASK 2.3
        # TASK 2.5
        if (command == "NAME"):
            socket.name = None
            for i in users:
                if (i.name == parameter):
                    message = "Username already taken, please try another using 'NAME username'"
                    message = message.encode()
                    socket.send(message)
                    socket.allowedMessages = False
                    print("Username invalid")
                    return True
            print("Username is ", parameter)
            socket.name = parameter
            socket.allowedMessages = True
            message = "Welcome to the chat " + socket.name
            socket.send(message.encode())
            
            for i in users:
                if (i == socket):
                    continue
                message = "(ALL) " + socket.name + " has joined the chat "            
                i.send(message.encode())
            return True

        if (socket.allowedMessages == False):
            message = "Please set a username using 'NAME username'"            
            socket.send(message.encode())
            return True

        elif (command == "LIST"):
            for i in users:
                name = "!" + str(i.name)
                name = name.encode()
                socket.send(name)

        
        elif (command == "ALL"):
            print("Message is ", parameter)
            for i in users:
                if (i == socket):
                    continue
                if (type(parameter) == str):
                    parameter = "(ALL) " + socket.name + ": " + parameter
                    parameter = parameter.encode()
                else:
                    parameter = parameter.decode()
                    parameter = "(ALL) " + socket.name + ": " + parameter
                    parameter = parameter.encode()
                i.send(parameter)

        elif (command == "MESSAGE"):
            (username, sep, message) = parameter.strip().partition(' ')
            print("User is ", username)
            print("Message is ", message)
            if (socket.name == username):
                message = "!You cannot send yourself a message."
                message = message.encode()
                socket.send(message)
                return True

            for i in users:
                if (i.name == username):
                    message = "(PRIVATE) " + socket.name + ": " + message
                    message = message.encode()
                    i.send(message)
                    return True
                    
            message = "!User not found, enter LIST to view live users"
            message = message.encode()
            socket.send(message)

        elif (command == "EXIT"):
            None
        
        else:
            message = "Invalid command, please try again"
            message = message.encode()
            socket.send(message)


        # Signify all is well
        return True

    def onDisconnect(self, socket):
        # TASK 2.1
        # TASK 2.2
        print("Client disconnected")
        global noUsers
        noUsers -= 1
        print("Live users = ", noUsers)
        global users
        users.remove(socket)
        for i in users:
            message = "(ALL) " + socket.name + " has left the chat."
            message = message.encode()
            i.send(message)

        
		  
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an echo server.
server = MyServer()


# Start server
server.start(ip, port)
