import socket

num1 = input("Enter first number: ")
num2 = input("Enter second number: ")
op = input("Enter operation (+, -, *, /): ")

data=f"{num1},{num2},{op}"

s=socket.socket()
s.connect(('localhost', 9999))

s.send(bytes(data,'utf-8'))
result=s.recv(1024).decode()
print(result)
s.close()