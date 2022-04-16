'''
Created on Jan. 31, 2022

@author: Phoebe Schulman, Ivan Lin
schu5560, linx8647 
'''

from socket import * 
import sys 
from struct import * 

import time
 
 #set up
serverName = 'localhost' #our server
#serverName='34.69.60.253' #debug server

serverPort = 12000 # Assign port number
clientSocket = socket(AF_INET, SOCK_DGRAM)# Bind socket to server address and server port- udp

def check_server_response(response): #debugging server
    data_len, pcode, entity = unpack_from('!IHH', response)
    if pcode==555:
        response = response[8:]
        print(response.decode())
        sys.exit()
    return 


print("CLIENT")
print ("\n------------ Starting Stage A  ------------ ")

#fill in info

data = "Hello World!!!"
data_length = len(data)

while (data_length%4 != 0): #padding
    data+= "\0" 
    data_length = len(data) #data_length+=1

data = data.encode("utf-8") #encoding data    
#print(data)

pcode = 0 #pcode = previous code
entity = 1 


#pack
head = pack("!IHH",data_length,pcode,entity) #header #!IHH -> big endian, int, short, short

packet = head+data
#print(packet)

#send packet
#print("client sending: \t data_length \t" +  str(data_length) + "\t pcode \t" +str(pcode)  + "\t entity \t" +str(entity)+ "\t data \t" +str(data.decode())) 

clientSocket.sendto( packet, (serverName, serverPort))

#recieve from server
received , serverAddress = clientSocket.recvfrom(2048)
#print('From server: ', received)

check_server_response(received) #debug server

#unpack
data_length,pcode ,entity,repeat, udp_port, len, codeA = unpack( "!IHHIIHH",received)


print("Received packet from server: data_length: " +  str(data_length) + " pcode: " +str(pcode)  + " entity: " +str(entity)+ " repeat: " +str(repeat)
     + " udp_port: " +str(udp_port) + " codeA: " +str(codeA)) 


#change ports
serverPort = udp_port # Assign port number
clientSocket = socket(AF_INET, SOCK_DGRAM)# Bind  socket to server address and server port

print ("------------ End of Stage A  ------------")


print ("\n------------ Starting Stage B  ------------")

packet_id = 0#1

while packet_id != repeat: #repeat the process
    
    #fill in info 
    
    data = bytearray(len)
    data_length = len
    
    while (data_length%4 != 0): #padding
        data.append(0)
        #data+= "\0" 
        data_length+=1 #data_length = len(data)
        
    
    data = pack("!I",packet_id) + data #need packet id in front of data
    data_length+=4 #

    pcode = codeA#0
    entity = 1 
       
    #pack
    head = pack("!IHH",data_length,pcode,entity) 
        
    packet = head+data 
    
    
    #send packet
    #print("Client sending: \t data_length \t" +  str(data_length) + "\t pcode \t" +str(pcode)  + "\t entity \t" +str(entity) + "\t packet_id \t" +str(packet_id) + "\t data \t" +str(data))

    clientSocket.sendto( packet, (serverName, serverPort))
    
    try:
        #recieve from server
        clientSocket.settimeout(5) #wait 5 secs to recive 
        
        received , serverAddress = clientSocket.recvfrom(2048)
        check_server_response(received) #debug server
        
        #only when non error: 
        
        #unpack
        data_length,pcode ,entity,acked_packet_id = unpack( "!IHHI",received)
        print("Received acknowledgement packet from server: data_len: " +  str(data_length) + " pcode: " +str(pcode)  + " entity: " +str(entity)+ " acknumber: " +str(acked_packet_id)) 
        
        packet_id+=1
    
    except:
        #check_server_response(received) #debug server
        print("time error")
        time.sleep(5) # wait 5 secs in between
    

#recieve from server #--last packet 
received , serverAddress = clientSocket.recvfrom(2048)
check_server_response(received) #debug server

#unpack
data_length,pcode ,entity,tcp_port,codeB = unpack( "!IHHII",received) #unpack( "!IHHIH",received) #codeB is short but will come as int?

#print("final packet\n")
print("Received final packet: data_len: " +  str(data_length) + " pcode: " +str(pcode)  + " entity: " +str(entity)+ " tcp_port: " +str(tcp_port) + " codeB: " +str(codeB)) 

print ("------------ End of Stage B  ------------\n")



print ("------------ Starting Stage C  ------------")
##chagne ports-tcp 

print("connecting to server at tcp port " + str(tcp_port))

time.sleep(3) #wait first

serverPort = tcp_port# Assign port number

clientSocket = socket(AF_INET, SOCK_STREAM)# Bind  socket to server address and server port- tcp
clientSocket.connect((serverName, serverPort))


#no send

#recieve from server
received , serverAddress = clientSocket.recvfrom(2048) 
check_server_response(received) #debug server

#unpack
data_length,pcode ,entity,repeat2,  len2, codeC, char = unpack( "!IHHIIIc",received) # c for char recive

char = char.decode()#convert byte aray to string

print("Received packet from server: data_len: " +  str(data_length) + " pcode: " + str(pcode)  + " entity: " + str(entity)+ " repeat2: " + str(repeat2)+" len2: " + str(len2)  + " codeC: " + str(codeC)   + " char: " + str(char)  ) 


print ("------------ End of Stage C  ------------\n")


print ("------------ Starting Stage D  ------------")


data = char*len2

print("Sending: " +  str(data) + " to server for " +  str(repeat2) + " times")


for i in range(repeat2): #repeat proces
    
    #fill in info 
    data = char*len2    
    data_length = len2
  
    while (data_length%4 != 0): #padding
        data+= "\0" #data.append(0)#
        data_length+=1 #data_length = len(data)
    
    data = data.encode("utf-8") #encoding data
    
    pcode = codeC
    entity = 1 
    
    #pack
    head = pack("!IHH",data_length,pcode,entity) 
    
    packet = head+data 
        

    #send packet
    #print("Client sending: \t data_length \t" +  str(data_length) + "\t pcode \t" +str(pcode)  + "\t entity \t" +str(entity) +  "\t data \t" +str(data))
    
    clientSocket.sendto( packet, (serverName, serverPort))
        
    time.sleep(0.1)
    
    
    
#recieve from server
received , serverAddress = clientSocket.recvfrom(1048) #2024

check_server_response(received) #debug server

#unpack
data_length,pcode ,entity,codeD= unpack( "!IHHI",received) 

print("Received from server: data_len: " +  str(data_length) + " pcode: " + str(pcode)  + " entity: " + str(entity) + " codeD: " + str(codeD)) 

#print ("\nend D=========\n")


clientSocket.close()

print ("\nend program")
