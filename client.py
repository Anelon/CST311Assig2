# The client sends a “ping” message package to the UDP server. Then UDP client waits for a second
# before retransmissions/sends another “ping” message package to the UDP server and it blocks the
# income “ping” message package. If it the UDP client has to wait longer than 1 second to
# retransmissions/resends another package, then this would result in loss of packages because the
# packages that were sent did not get sent back. This program calculates and prints the minimum,
# maximum, and average RTTs at the end of all pings from the client, the number of packets lost
# and the packet loss rate (in percentage).  It also computes and prints the estimated RTT,
# DevRTT, and the TimeoutInterval based on the RTT results.

from __future__ import division #uses division format
from socket import *  # import socket interfaces
from time import  time
from statistics import mean
from datetime import datetime
serverName = 'localhost'  # server ip for computers
serverPort = 12000 # server port number
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1) #sets time out for 1 second and blocks the incoming data package
                            # for checking connection and package loss
sequence_number = 1
TimeoutInterval = 0
DevRTT = 0
EstimatedRTT = 0
lostPackages = 0
minRTT = -1
maxRTT = -1
total = 0
address = serverName

# You should get the client to wait up to one second for a reply; if no reply
# is received within one second, your client
# program should assume that the packet was lost during transmission across the
# network https://docs.python.org/3/library/socket.html

while sequence_number < 11:
    message = "Ping"
    start_time = datetime.now().microsecond/1000
    # the client sends the message to the server, the client sends the ping message to the server
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    try:
        message, address = clientSocket.recvfrom(1024) # message and address is received from the server, the client gets ping back
        end_time = datetime.now().microsecond/1000  #end time
        SampleRTT = end_time-start_time #round trip time for the UPD client to send “ping” and get the “ping” message back
        print("Server responded: Round trip time (RTT) =", SampleRTT)
        if minRTT == -1:
            minRTT = SampleRTT
        if maxRTT == -1:
            maxRTT = SampleRTT
        if SampleRTT < minRTT:
            minRtt = SampleRTT
        if SampleRTT > maxRTT:
            maxRTT = SampleRTT
        total += SampleRTT

        #(Then compute and print what should be the timeout period based on the RTT results.)
        #(10 %) Calculate and print the estimated RTT. Consider alpha = 0.125.
        #Formula: EstimatedRTT = (1- 0.125)*EstimatedRTT + 0.125*SampleRTT

        EstimatedRTT = 0.875*EstimatedRTT + 0.125*SampleRTT
        print("EstimatedRTT =", EstimatedRTT)

        #( (10 %) Calculate and print DevRTT. Consider beta = 0.25. Calculate and print Timeout interval.

        #estimate SampleRTT deviation from EstimatedRTT Formula: DevRTT = (1-0.25)*DevRTT +  0.25*|SampleRTT-EstimatedRTT|
        #if DecRTT is a small value then RTT is constant if not then RTT is inconstant.
        DevRTT = 0.75*DevRTT + 0.25*abs(SampleRTT-EstimatedRTT)

        print("DevRTT =", DevRTT)

        TimeoutInterval = EstimatedRTT + 4*DevRTT
        print("TimeoutInterval  =", TimeoutInterval)

    except: #catches the exception errors so the program doesn’t crush of the client socket.settimeout(1), if there’s connection problems, and the timeout is longer than 1 second then it results in losing packages and udp waits for retransmission
        print( "Request timed out")
        lostPackages +=1

        #package lost percentages =( packets lost)/(# packet sent).
    finally:
        if sequence_number == 11 :
            clientSocket.close()  #closes connection
            percentage = "{0:.0f}%".format((lostPackages/sequence_number)*100)
    percentage = "{0:.0f}%".format((lostPackages/sequence_number)*100)
    print("Ping statistics for", address)
    print("Packets: Sent =", sequence_number, "Received =", sequence_number - lostPackages, "Lost = ", lostPackages, "(", percentage, "loss),")
    sequence_number +=1

#( Your client software will need to determine and print out the minimum, maximum, and average RTTs at the end of all pings from the client along with printing out the number of packets lost and the packet loss rate (in percentage).  Then compute and print what should be the timeout period based on the RTT results. )
avgRTT = total/sequence_number
#print("Packets: Sent =", sequence_number, "Received =", sequence_number - lostPackages, "Lost = ", lostPackages, "(", percentage, "loss),")
print("Approximate round trip times in milli-seconds:")
print ("Minimum =", '{0:.2f}'.format(minRTT),"ms, Maximum =",'{0:.2f}'.format(maxRTT),"ms Average =", '{0:.2f}'.format(avgRTT),"ms")
