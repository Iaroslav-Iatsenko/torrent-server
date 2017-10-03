import socket


#  test connection between client and server on port 8080
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 8080))
    s.listen(1)
    sock, client = s.accept()
    data = sock.recv(1048576)

    sock.close()
    s.close()

    #  to see data on the terminal printing it by uncomment this
    # print(data)

    #  receiving a file from client / remove utorrent.png from resources before testing
    with open('tests/resources/utorrent.png', 'wb') as image_file:
        image_file.write(data)
