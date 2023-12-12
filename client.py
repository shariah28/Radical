import threading  #Import the threading module
from socket import *  # Import everything from the socket module

#Variable that holds the localhost server IP, 172.0.0.1
serverName = 'localhost'
serverPort = 12000 #Port number used by server
clientSocket = socket(AF_INET, SOCK_STREAM) #Create a socket object
clientSocket.connect((serverName, serverPort)) #Connect to the server

#Function used to receive messages from the server
def receive_messages(connection): #connection is the socket object that holds the connection to the server
    while True:  #While loop used to receive messages from the server
      #Error handling used to capture any potential errors faced when transmitting messages.
        try:
            message = connection.recv(1024).decode() # Receive the message from the server in size 1024 bytes
            print(message) #Print message to terminal from server.
        except:
            # Handle errors or a closed connection
            print("You have been disconnected from the server.") #Error message
            break #Breaks loop after sending error message

username = input('Enter your username: ') #Ask client to enter their username
clientSocket.send(username.encode()) #Sends username to the server

# Start a thread to keep receiving messages from server
threading.Thread(target=receive_messages, args=(clientSocket,)).start()

# Send messages
while True: #While loop used to keep the client receiving messages from the server until they disconnect
    message = input('') #Ask the client to type a message
    if message == "quit":  #If client types quit, break the loop
        break
    clientSocket.send(message.encode()) #Send the message to the server for other clients to see

# Close the connection
clientSocket.close()