import socket

num=input("Enter your GPA: ")
num=float(num)

s=socket.socket()
s.connect(('localhost', 9999))
s.send(bytes(str(num),"utf-8"))

resp=s.recv(1024).decode()
print("Server response:", resp)
s.close()