# aws-python-chat

Regular simple chat based on sockets. Was installed on AWC EC2 instance. Security groups were configured for proper connection on the client side.

The main idea is that on the cloud the script monitors the logs for errors and if it finds one, the server reboots.

### How it works:

Server Start: When you run the server.py script, you create a server socket that listens for incoming connections on a specific port (in this case, port 8080). The main program thread is also started.
Client Listening: The main server stream is waiting for clients to connect. Once the client is connected, a new thread (or process, depending on the implementation) is created for the client. This allows you to serve multiple customers simultaneously.

![image](https://github.com/this-is-yally/aws-python-chat/assets/79525614/002484f9-e43c-4b71-903b-2a8c0a0756e0)


Messaging: Each client has its own socket to communicate with the server. The server and the client can send messages to each other via these sockets. Messages are sent as strings and can be of any length.

![image](https://github.com/this-is-yally/aws-python-chat/assets/79525614/36c0681e-2b2c-43a0-8b1a-c4fea8aa1bb3)

Logging: The Server writes all incoming messages from clients to the server.log file. This allows you to keep a history of communication between clients and the server, as well as to discover the keyword "exit".

![image](https://github.com/this-is-yally/aws-python-chat/assets/79525614/1ea0bf5a-d1f4-4d53-b824-d9c89e333033)

Key Discovery "exit": Script.sh* periodically monitors the server.log log file for the keyword "exit". If this word is found, it means that one of the clients requested the end of the session. In this case, the script performs the following actions:

![image](https://github.com/this-is-yally/aws-python-chat/assets/79525614/0bddc028-5e81-47bc-bb0b-a92378b6e18a)

  _1. Stops the currently running server process using the pkill command.
  2. Waiting two seconds to make sure all the resources are available.
  3. Verifies whether port 8080 is used by another process using lsof.
  4. If the port is still in use, the script completes the process on port 8080.
  5. Waits 10 seconds before restarting the server using python3.
  6. Starting the server again: After all checks and waits, the script restarts the server so that it can again listen on port 8080 and serve clients.

Cyclic check: This process is repeated cyclically, allowing the server and clients to communicate for a long time, and the server monitoring script automatically restarts the server if it detects end-of-session requests._


*_I added a second version of the script that checks if the server is running, and if the server is shut down for any other error, the script automatically restarts it. In the first version I showed exactly the work with the log file._
