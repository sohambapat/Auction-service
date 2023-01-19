#Name: Soham Bapat
#Unity ID: sbapat2

import socket
import threading

IP = socket.gethostbyname(socket.gethostname()) #Set IP Address using hostname
PORT = 9999 #Using a high number port number 
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8" #Mentioning format 
DISCONNECT_MSG = "!DISCONNECT"

#Declaring variables
type=None
min_price = None
noofbids=0
name=None
bids = [] 
allbidsrcvd = False
seller_ip=None
winner_ip=None
addrs = []

def handle_client(conn, addr, activeCount):

    #Declaring global variables so that they can be accessed inside the function
    global type
    global min_price
    global noofbids
    global name
    global bids
    global allbidsrcvd
    global seller_ip
    global winner_ip
    global addrs

    print(f"[NEW CONNECTION] {addr} connected.")
    addrs.append(addr) #Add addresses that are connected to a list to be referenced later

    sellinfo = False #Boolean variable for checking if seller has added the item information
    connected = True
    

    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG: #If disconnect message is triggered, close the connection
            connected = False

        print(f"[{addr}] {msg}")
        #Check if anyone is connected to the port. If no one is connected, the first connection is the seller.
        if activeCount == 0: 
            if sellinfo: 
                if allbidsrcvd: #Check if all bidders have bid. If so, announce the winner
                    winner = str(closeAucBid(type, bids))
                    amount = str(closeAucBidAmount(type, bids))
                    msg3 = f"The winner of {name} is bidder {winner} and amount due is ${amount}. IP Address is {addrs[(int(winner)-1)]}"
                    conn.send(msg3.encode(FORMAT))
                else:
                    msg1 = "Waiting for buyers...Type something and enter to get an update or enter '!DISCONNECT' to disconnect from server."
                    conn.send(msg1.encode(FORMAT))
            else: #If seller info has not been added, prompt the user to add it
                msg = "You are the seller. Please give item and auction details: \n Please input the following: type, min price, #of bids, name"
                seller_ip = addr
                conn.send(msg.encode(FORMAT))
                rmsg = conn.recv(SIZE).decode(FORMAT)
                type, min_price, noofbids, name = rmsg.split(' ')  #Split the input into respective variables
                msg1 = "Auction started...Type anything and press enter to get an update." #Begin the auction
                conn.send(msg1.encode(FORMAT))
                sellinfo=True  #Set the sell info as true since it was given by the seller
                
        elif activeCount < int(noofbids):

            if allbidsrcvd:
                winner = str(closeAucBid(type, bids))
                amount = str(closeAucBidAmount(type, bids))
                if addrs[(int(winner))] == addr:
                    msg3 = f"You win! Expect the file from the seller with IP: {addrs[(0)]}"
                else:
                    msg3 = f"The winner of {name} is bidder {winner} and amount due is ${amount}."
                conn.send(msg3.encode(FORMAT))

            else:
                msg = f"You are bidder {activeCount}. Please give your bid. The minimum bid is {str(min_price)} :" #Take in the bid from the buyer
                conn.send(msg.encode(FORMAT))
                rmsg1 = conn.recv(SIZE).decode(FORMAT)

                print("Bid " + str(activeCount) + " received: $" + rmsg1)

                bids.append(int(rmsg1)) #Add the bid to the array
                msg1 = "Bid received. Type and enter something for an update on the bid."
                conn.send(msg1.encode(FORMAT))

        elif activeCount == int(noofbids):  #Once we have received the correct number of bids, set all bids received as true
            
            if allbidsrcvd:
                winner = str(closeAucBid(type, bids))
                amount = str(closeAucBidAmount(type, bids))
                if addrs[(int(winner))] == addr:
                    msg3 = f"You win! Expect the file from the seller with IP: {addrs[(0)]}"
                else:
                    msg3 = f"The winner of {name} is bidder {winner} and amount due is ${amount}."
                #msg3 = f"The winner of {name} is bidder {winner} and amount due is ${amount}"
                conn.send(msg3.encode(FORMAT))


            else:
                msg = f"You are bidder {activeCount}. Please give your bid. The minimum bid is {str(min_price)} :"
                conn.send(msg.encode(FORMAT))
                rmsg1 = conn.recv(SIZE).decode(FORMAT)
                print("Bid " + str(activeCount) + " received: $" + rmsg1)
                bids.append(int(rmsg1))
                msg1 = "Bid received. Type and enter something for an update on the bid."
                conn.send(msg1.encode(FORMAT))

                allbidsrcvd = True #Set all bids received as true

        else: #If the connection exceeds the number of active connections allowed for the bid, display this message
            msg = "Currently busy, wait for auction to end and try again in some time."
            conn.send(msg.encode(FORMAT))
            
            

    conn.close()

def closeAucBid(type, bids): #This function checks for the type of auction and returns the bidder who won
    winner = 0
    secondplace = 0
    for i in bids:
        if int(i) >  int(winner):
            winner = i
    return (bids.index(winner)+1)

def closeAucBidAmount(type, bids):
    winner = 0
    secondplace = 0
    if(type == '1'):
        for i in bids:
            if int(i) >  int(winner):
                winner = i
        return winner
    else:
        for i in bids:
            if int(i) >  int(winner):
                secondplace = winner
                winner = i
        return secondplace


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    

    while True: #Accept new connections to the port and print current active connections
        conn, addr = server.accept() 
        thread = threading.Thread(target=handle_client, args=(conn, addr, (threading.activeCount()-1)))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()