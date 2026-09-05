import socket
s=socket.socket()
s.bind(('localhost', 9999))
s.listen(5)
print("Server is listening on port 9999...")

while True:
    c, addre=s.accept()
    print("got connection from", addre)
    data = c.recv(1024).decode()
    print("Received data:", data)
    if not data:
        c.close() 
        continue

    gp=float(data)
    if gp >= 4.33:
        result = "Letter Grade: A+ | Qualification: Excellent"
    elif gp >= 4.00:
        result = "Letter Grade: A  | Qualification: Excellent"
    elif gp >= 3.66:
        result = "Letter Grade: A- | Qualification: Very good"
    elif gp >= 3.33:
        result = "Letter Grade: B+ | Qualification: Very good"
    elif gp >= 3.00:
        result = "Letter Grade: B  | Qualification: Very good"
    elif gp >= 2.66:
        result = "Letter Grade: B- | Qualification: Good"
    elif gp >= 2.33:
        result = "Letter Grade: C+ | Qualification: Good"
    elif gp >= 2.00:
        result = "Letter Grade: C  | Qualification: Good"
    elif gp >= 1.66:
        result = "Letter Grade: C- | Qualification: Passable"
    elif gp >= 1.33:
        result = "Letter Grade: D+ | Qualification: Passable"
    elif gp >= 1.00:
        result = "Letter Grade: D  | Qualification: Passable"
    else:
        result = "Letter Grade: E  | Qualification: Failure"
    c.send(bytes(result, "utf-8"))
    c.close()