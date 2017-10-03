import socket


#  test connection between client and server on port 8080
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 8080))
    s.listen(1)
    sock, client = s.accept()
    data = sock.recv(1024)
    sock.close()
    s.close()
    print(data)
