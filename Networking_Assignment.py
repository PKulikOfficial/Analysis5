##################
## MADE BY:     ##
## Patryk Kulik ##
## 0989317      ##
## INF2D        ##
##################

# Importing needed modules
import socket
import json
import sys

# School Server parameters
PORT = 55550
SERVER_IP = "145.24.222.133"
ADDR = (SERVER_IP, PORT)

#Client 2 Server parameters
CLIENT2_PORT = 44400
CLIENT2_IP = sys.argv[1]
CLIENT2_ADDR = (CLIENT2_IP, CLIENT2_PORT)

#Getting current PC IP for message
MY_IP = socket.gethostbyname(socket.gethostname())

#Client 1
def Client1():
    #Connecting to server
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1.connect(ADDR)

    #Getting welcome message from server
    print(repr(client1.recv(1024)))
    
    #Creating, encoding & sending  my message to server
    my_msg =  {
        "studentnr1" :  "0989317",
        "studentnr2" :  "0989317",
        "classname" :   "INF2D",
        "clientid" :    int(sys.argv[2]),
        "teamname" :    "Patryk",
        "ip" :          MY_IP,
        "secret" :      "",
        "status" :      ""
    }
    my_msg_encoded = json.dumps(my_msg).encode('utf-8')
    client1.send(my_msg_encoded)

    #Receiving message back
    server_msg = client1.recv(2000)
    server_msg_decoded = json.loads(server_msg.decode('utf-8'))
    print(server_msg_decoded)

    #Closing connection with school server
    client1.close()

    #Checking if status == waiting for message 2
    if server_msg_decoded.get("status") == "waiting for message 2":
        #Connecting to client 2
        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Checking if client2 is up -> when check_status returns 0, it means the client2 is running
        check_status = client1.connect_ex(CLIENT2_ADDR)
        while check_status != 0:
            check_status = client1.connect_ex(CLIENT2_ADDR)
            print("Trying to connect to client 2" + str(CLIENT2_ADDR))

        #Sending the message and close the connection with client 2
        print("You connected with client 2. Sending the message...")
        client1.sendall(server_msg)
        client1.close()
    else:
        print("Wrong message received, terminating the process")

#Client 2
def Client2():
    #Setting up client 2 to receive message 
    SERVER_CLIENT2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_CLIENT2.bind(CLIENT2_ADDR)

    #Listening for connection & message
    print("Listening")
    SERVER_CLIENT2.listen()
    while True:
        conn, addr = SERVER_CLIENT2.accept()
        recv_msg = conn.recv(2000)
        recv_msg_decoded = json.loads(recv_msg.decode('utf-8'))
        break
    SERVER_CLIENT2.close()

    #Getting message received from client1
    print("\nReading received message from client 1" + str(addr) + ": \n" + str(recv_msg_decoded) + "\n")

    #Changing values of client 1 message
    my_client2_msg = recv_msg_decoded

    #Swapping student numbers and changing other values
    temp = my_client2_msg["studentnr1"]
    my_client2_msg["studentnr1"] = my_client2_msg["studentnr2"]
    my_client2_msg["studentnr2"] = temp

    my_client2_msg["clientid"] = int(sys.argv[2])
    my_client2_msg["ip"] = MY_IP

    #Connecting to school server
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2.connect(ADDR)

    #Getting welcome message from server
    print(repr(client2.recv(1024)))

    #Encoding new message to send to server
    my_client2_msg_encoded = json.dumps(my_client2_msg).encode('utf-8')
    client2.sendall(my_client2_msg_encoded)

    #Receiving & reading final message
    server_msg_final = client2.recv(2000)
    server_msg_final_decoded = json.loads(server_msg_final.decode('utf-8'))
    print(server_msg_final_decoded)

    #Closing connection with school server
    client2.close()


# Checking which client the program should run
# Client 1 example -> C:\Users\Patryk\Desktop>py 0989317_NETW_ASSIGNMENT.py 192.168.1.10 1
# Parameter 1 -> SHOULD ALWAYS BE THE IP OF CLIENT 2 !!!
# Parameter 2 -> CHOOSE WHICH CLIENT YOU WANT TO RUN (EITHER '1' or '2')
if sys.argv[2] == "1":
    Client1()
elif sys.argv[2] == "2":
    Client2()
else:
    print("Client does not exist")
