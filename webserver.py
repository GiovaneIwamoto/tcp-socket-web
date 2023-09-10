# Web server supports one file request.
# Use it in a web browser as "localhost:6789/index.html"

# Import socket module
from socket import * 
import sys # In order to terminate the program

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 6789

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
	print("📞 The Server is Ready to Receive")

	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()  

	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
	
	try:
		# Receives the request message from the client
		message = connectionSocket.recv(1024).decode()
		
		print ("✅ Passed the Accept")
		
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		filename = message.split()[1]
		
		# Because the extracted path of the HTTP request includes 
		# a character '\', we read the path from the second character
		print ("📁 File: ", filename)
		if filename == "/favicon.ico": continue
		
		f = open(filename[1:])
		
		# Store the entire content of the requested file in a temporary buffer
		outputdata = f.read()
		
		# Send the HTTP response header line to the connection socket
		connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode()) 
 
		# Send the content of the requested file to the connection socket
		for i in range(0, len(outputdata)):  
			connectionSocket.send(outputdata[i].encode())
		connectionSocket.send("\r\n".encode()) 
		
		# Close the client connection socket
		print ("🛡️ Closing Connection Socket")
		connectionSocket.close()

	except IOError:				
		print("⛔ IO Error")
			
		# Send HTTP response header line for file not found (404)
		connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
		connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
			
		# Close the client connection socket
		connectionSocket.close()

serverSocket.close()  
sys.exit() #Terminate the program after sending the corresponding data