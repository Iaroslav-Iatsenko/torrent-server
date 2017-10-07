from server import SimpleTorrentServer


def main():
    #  testing server-client connection works
    server = SimpleTorrentServer()
    server.fulfill()


if __name__ == "__main__":
    main()
