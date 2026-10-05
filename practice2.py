import socket
i=input("enter..")
data="3,2,+"
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(('localhost',9998))
s.sendto(bytes(data,'utf-8'))
result=s.recvfrom(1024)[0].decode()
print(result)