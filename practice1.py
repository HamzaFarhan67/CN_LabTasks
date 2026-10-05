import socket

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost',9998))
s.listen(3)

while True:
    c,addr=s.accept()
    data=c.recvfrom(1024)[0].decode()
    num1,num2,op=data.split(",")
    num1=int(num1)
    num2=int(num2)
    if op=="+":
        result=num1+num2
    elif op=="-":
        result=num1-num2
    elif op=="*":
        result=num1*num2
    elif op=="/":
        result=num1/num2
    f=open("logg.txt","a")
    f.write(f"client sent {num1}, {num2}, {op}")
    f.close()

    c.send(bytes(num1,'utf-8'))
    