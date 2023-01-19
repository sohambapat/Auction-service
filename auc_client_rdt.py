#Name: Soham Bapat
#Unity ID: sbapat2

import time
import socket

IP = socket.gethostbyname(socket.gethostname()) #Set IP Address using hostname
PORT = 9999 #Using a high number port number
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8" #Mentioning format 
DISCONNECT_MSG = "!DISCONNECT"
counter = 0
isSeller = False
isBuyer = False
count = 0

#Declares keywords to identify buyer and seller
seller_word = "You are the seller"
seller_send = "IP Address is"
buyer_word = "You are bidder"
winner_msg = "You win!"

def main():
    #Declare global variables
    global winner_ip
    global winner_port
    global seller_ip
    global seller_port
    global WINNER_ADDR
    global SELLER_ADDR
    global isBuyer
    global isSeller
    global count

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates a socket
    client.connect(ADDR)

    #Sends a message in terminal when client connects to the server on the associated IP and Port
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT} - Type anything to continue: ")

    connected = True
    while connected:
        #Set an input channel
        msg = input("> ")
        client.send(msg.encode(FORMAT))

        #Take input from the server if the message is not the disconnect message
        if msg == DISCONNECT_MSG:
            isBuyer = False
            isSeller = False
            connected = False
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            #if the client is seller
            if seller_word in msg:
                isSeller = True
            
            if seller_send in msg: #close the connection with the server after the auction is over
                connected = False


            #if the client is buyer
            if buyer_word in msg:
                isBuyer = True

            if winner_msg in msg: #close the connection with the server when the auction is over
                connected = False
                client.close()
                

            print(f"[SERVER] {msg}")
    
    #If the client is the seller, it sends the file to the buyer
    if isSeller: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print ("Sending")

        f = open("hello.txt", "r")
        data = f.read(2000)
        while(data):
            count = count+1
            sock.sendto(data.encode(), (IP, int(PORT)))
            data = f.read(2000)
            time.sleep(0.02) # Give receiver a bit time to save
            print(f"Sending packet chunk {count+1}")
        print("Finished sending file! Closing connection...")
        sock.close()
        f.close()

    #If the client is the buyer, it receives the file from the seller
    if isBuyer:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((IP, int(PORT)))
        print(f"Listening on {IP}:{PORT}")

        while True:
            data, addr = sock.recvfrom(2000) #Receives file over the binded socket
            if data:                         #If the file date is received from the seller, create a new file and add the data to it.
                print (f"File data received.")
            f = open("hello_new.txt", 'w+')
            f.write(str(data))
            
            print("Finished copying data to new file")
            f.seek(0)
            print(f"Displaying content data....\n {f.read()}")     #Print the data from the new file 
            f.close()

            break


if __name__ == "__main__":
    main()