import socket

s=socket.socket()
s.bind(('localhost', 9999))
s.listen(5)
print('Server is listening...')

while True:
    c, addr= s.accept()
    print('Got connection from', addr)
    data=c.recv(1024).decode()
    print('Received data:', data)
    if not data:
        c.close()
        break
    num1,num2,op=data.split(",")
    num1=int(num1)
    num2=int(num2)
    if op == '+':
            res = num1 + num2
    elif op == '-':
        res = num1 - num2
    elif op == '*':
        res = num1 * num2
    elif op == '/':
        res = num1 / num2 if num2 != 0 else "Error: Division by zero"
    else:
        res = "Error: Invalid operator"
    f=open("history.txt","a")
    f.write(f"client {num1} {op} {num2} = {res}\n")
    f.close()

    c.send(bytes(f"result: {res}",'utf-8'))