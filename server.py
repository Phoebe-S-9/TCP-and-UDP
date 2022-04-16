'''
Created on Jan. 31, 2022

@author: Phoebe Schulman, Ivan Lin
schu5560, linx8647 
'''

from socket import * 
import sys 
from struct import * 

import time

import random #rand nums
 
 #set up
 
 # starts running on UDP port 12000 
serverPort = 12000 #port num
serverSocket = socket(AF_INET,SOCK_DGRAM) #sockdgram->udp
serverSocket.bind(("", serverPort)) #bind server adress and server port


TIME_OUT = 3 #100#3 #3 secs

print("SERVER\n")
#print ("------------ Starting Stage A  ------------\n")

serverSocket.settimeout(TIME_OUT)#verify - time out 


#fill in info #expected
data_expected = "Hello World!!!"
data_length_expected = len(data_expected)

while (data_length_expected%4 != 0): #padding
    data_expected+= "\0" 
    data_length_expected = len(data_expected) #data_length+=1

data_expected= data_expected.encode("utf-8") #encoding data    
#print(data)

pcode_expected = 0 #pcode = previous code
entity_expected = 1

'''
data = "Hello World!!!"
data_length = len(data)

while (data_length%4 != 0): #padding
    data+= "0" 
    data_length = len(data) #data_length+=1

data = data.encode("utf-8") #encoding data    
#print(data)

pcode = 0 #pcode = previous code
entity = 1
'''

#recieve from client
received, clientAddress = serverSocket.recvfrom(1024) 

try:#verify?
    data_length,pcode ,entity = unpack( "!IHH",received[:8])
    data= received[8:]
    print("receiving from the client: data_length: " +  str(data_length) + " code: " +str(pcode)  + " entity: " +str(entity)+ " data: " +str(data.decode()))
    #validation kind of
    assert data == data_expected and pcode == pcode_expected and data_length == data_length_expected

except:
    print("bad input-format, system exit")
    serverSocket.close()  
    sys.exit()


if data_expected!= data or data_length!=data_length_expected or pcode_expected !=pcode or entity_expected!=entity: #verify?
    print("bad input - values")
    sys.exit() #leave?

print ("\n------------ Starting Stage A  ------------\n")

#fill in info #assign random 
entity = 2 #server

repeat = random.randint(5,20)  #random.randint(5,20) #5
udp_port = random.randint(20000,30000)
len = random.randint(50,100) #short
codeA = random.randint(100,400) #short

#pack
packet =  pack("!IHHIIHH",data_length,pcode ,entity,repeat,udp_port,len,codeA)#

#send packet
serverSocket.sendto(packet, clientAddress)
print("sending to the client: data_length: " +  str(data_length) + " code: " +str(pcode)  + " entity: " +str(entity)+ " repeat: " +str(repeat)
     + " udp_port: " +str(udp_port)  + " len: " +str(len)  + " codeA: " +str(codeA)) 


#change ports
serverPort = udp_port#12000 #port num
serverSocket = socket(AF_INET,SOCK_DGRAM) #sockdgram->udp

serverSocket.bind(("", serverPort)) #bind server adress and server port

print('SERVER: Server ready on the new UDP port: ' + str(udp_port) )

print ("\nSERVER:------------ End of Stage A  ------------\n")



print ("SERVER:------------ Starting Stage B  ------------")

acked_packet_id = 0 #server
wil_ack = 0;#if servser will acknowldge


#verify stuff...
    
packet_id = 0#1 #expected


while acked_packet_id!= repeat: #packet_id != repeat: #repeat the process
    
    #fill in info #expected  #if data len!= expected -> errror
    data = bytearray(len)
    data_length_expect = len
    #data_length = len
    
    while (data_length_expect%4 != 0): #padding
        data.append(0)#data+= "\0" 
        data_length_expect+=1 #data_length = len(data)
        
    
    #data = pack("!I",packet_id) + data #need packet id in front of data
    data_length_expect+=4 #
    pcode = codeA#0
    entity = 1 
    #recieve from client
    received, clientAddress = serverSocket.recvfrom(1024) 

  
    try:#verify?
    
        data_length,pcode ,entity = unpack( "!IHH",received[:8])
        data= received[8:]
        packet_id= data[:4]#.decode() #packet id in the data- start of it  #first 4 bytes of data??
        #packet_id= data[:1]#.decode()  
        assert data_length == data_length_expect
        will_ack = random.randint(0,20)
        if(will_ack>5):#over a threshold
           
            print("SERVER: received_packet_id = "+ str(acked_packet_id) + " data_len = " +  str(data_length) + " pcode: " +str(pcode))

                        
            #assign random #not need
            pcode = codeA
            entity = 2 #server
    
            #pack
            packet =  pack("!IHHI",data_length,pcode ,entity,acked_packet_id)
            
            #send
            serverSocket.sendto(packet, clientAddress)
    
            #print("Sending: \t data_length \t" +  str(data_length) + "\t pcode \t" +str(pcode)  + "\t entity \t" +str(entity)+ "\t acked_packet_id \t" +str(acked_packet_id))
    
            acked_packet_id+=1
        
        
        else:
             print("(ignored packet)")

            
    except:
        print("bad input-format, system exit")
        serverSocket.close()  
        sys.exit()


#  #assign random     
tcp_port = random.randint(20000,30000) 
codeB = random.randint(100,400) #short

#send last packet
packet = pack( "!IHHII",data_length,pcode ,entity,tcp_port,codeB )
serverSocket.sendto(packet, clientAddress)


#print("final packet\n")
#print("Sending: \t data_length \t" +  str(data_length) + "\t pcode \t" +str(pcode)  + "\t entity \t" +str(entity)+    "\t tcp_port \t" +str(tcp_port) + "\t codeB \t" +str(codeB)) 
print(" ------------- B2: sending tcp_port " + str(udp_port) + " codeB " + str(codeB))
print (" ------------ End of Stage B  ------------")


print ("\n ------------ Stating Stage C ------------")
##chagne ports-tcp 

print(" The server is ready to receive on tcp port:  " + str(tcp_port))

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = tcp_port# Assign port number
serverSocket.bind(("", serverPort))# Bind the socket to server address and server port

serverSocket.listen(5)# Listen to at most 1 connection at a time-tcp only #sever listen and clinet connects

# Set up a new connection from the client # tcp
connectionSocket, addr = serverSocket.accept()


pcode = codeB
entity = 2 #server

#assign random     
repeat2 = random.randint(5,20) 
len2 = random.randint(50,100) #short
codeC = random.randint(100,400) #short


char = 'm'.encode()#byte arry #char= 'm' #rand letter?

#pack and send
packet = pack( "!IHHIIIc",data_length,pcode ,entity,repeat2,  len2, codeC, char )# c for char recive


#serverSocket.sendto(packet, clientAddress)-udp
connectionSocket.send(packet) #tcp

print(" Server is sending to the client:  data_length: " +  str(data_length) + " code: " + str(pcode)  + " entity: " + str(entity)+ " repeat2: " + str(repeat2)+" len2: " + str(len2)  + " codeC: " + str(codeC)) 


#no recieve from cleint

print (" ------------ End of Stage C    ------------\n")


print (" ------------ Starting Stage D  ------------")


data = char*len2

#print("Reciving: " +  str(data) + " to server " +  str(repeat2) + " times")
print("Starting to Receive packets from client")

for i in range(repeat2): #repeat proces
    #fill in info #expected
    data = str(char*len2) #data = char*len2    
    data_length = len2
  
    while (data_length%4 != 0): #padding
        data+= "\0" #
        #data.append(0)#
        data_length+=1 #data_length = len(data)
    
    data = data.encode("utf-8") #encoding data
    
    pcode = codeC
    entity = 1 
    
    #also timeout check ?
    
    #recieve from client
    #received, clientAddress = serverSocket.recvfrom(1024) #upd recive
    received = connectionSocket.recv(1024)#.decode() #tcp recieve
    
    
    try:#verify?
        data_length,pcode ,entity = unpack( "!IHH",received[:8])
        data= received[8:]
    except:
        print("bad")
    print("i = " + str(i) + " data_len: " + str(data_length) + " pcode: " + str(pcode) + " entity: " + str(entity) + " data: " + str(data.decode()))
   
#fil info   
pcode =codeC
entity = 2 #server  

#rand     
codeD = random.randint(100,400) #short

#pack
packet =  pack("!IHHI",data_length,pcode ,entity,codeD)

    
#send from server

#serverSocket.sendto(packet, clientAddress) #udp send
connectionSocket.send(packet) #tcp send

#print("Sending: \t data_length \t" +  str(data_length) + "\t pcode \t" +str(pcode)  + "\t entity \t" +str(entity)+ "\t data \t" +str(data))
    

#print ("\nend D=========\n")


print ("\nend program")
connectionSocket.close()#tcp
serverSocket.close()  
sys.exit()


'''p = bytearray(1)
 print(p)
 print(str(p))
 print(str(p.decode()))
 '''
