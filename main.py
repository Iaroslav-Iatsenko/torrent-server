from server import SimpleTorrentServer


def main():
    #  testing server-client connection works
    server = SimpleTorrentServer()
    server.run()


if __name__ == "__main__":
    main()
