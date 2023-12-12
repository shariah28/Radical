import threading  #Import the threading module
from socket import *  #Import everything from the socket module

serverPort = 12000 #Port number used by server
serverSocket = socket(AF_INET, SOCK_STREAM) #Create a TCP socket object
serverSocket.bind(('', serverPort)) #Bind the socket to the port
serverSocket.listen() #Listen for connections
print('The server is ready to receive') #Message that states the server is ready to receive

clients = [] #Create an empty list to hold the clients
usernames = [] #Create an empty list to hold the usernames

#client_thread function that will be called when a client connects to the server
def client_thread(connection, addr): #connection is the socket object, addr is the address of the client
    username = connection.recv(1024).decode() #Receive the username from the client
    usernames.append(username) #Adds the username to the list of usernames
    clients.append(connection) #Adds the client to the list of clients
    print(f"{username} has connected from {addr}") #Prints a message to the terminal to let the user know that the client has connected

  #While loop used to broadcast client messages to the server for all to see.
    while True:
      #error handling used to capture any potential errors faced when transmitting messages.
        try:
            message = connection.recv(1024).decode() #Receive the message from the client in size 1024 bytes
            broadcast_message(message, username) #Broadcasts message to server with the username of the client
        except:
            # Remove client when they disconnect or an error occurs
            index = clients.index(connection) #Get the index of the client in the list of clients
            clients.remove(connection) #Remove the client from the list of clients
            username = usernames[index] #Get the username of the client
            usernames.remove(username) #Remove the username from the list of usernames
            connection.close() #Close the connection
            print(f"{username} has disconnected.") #Print a message to the terminal to let the user know that the client has disconnected
            break #Breaks loop after sending error message

#broadcast_message function that will be called to broadcast messages to the server for all to see
def broadcast_message(message, username=""): #message is the message that the client sent, username is the username of the client
    for client in clients: #For loop used to broadcast the message to all the clients
        #error handling used to capture any potential errors faced when transmitting messages.
        try:
            client.send(f"{username}: {message}".encode()) #Send the message to the client in size 1024 bytes
        except:
            # Handle a client that has closed the connection
            clients.remove(client)
          
#While loop used to accept and create thread to handle the client
while True:
    connectionSocket, addr = serverSocket.accept() #Accept the connection from the server
    thread = threading.Thread(target=client_thread, args=(connectionSocket, addr)) #Create a thread to handle the client
    thread.start() #Start the thread
