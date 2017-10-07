import asyncio


@asyncio.coroutine
def handle_client(client_reader, client_writer):
    # let the client know they are connected
    print("Send: Connection established")
    client_writer.write("Connection established".encode())

    # give client a chance to respond, timeout after 10 seconds
    data = yield from asyncio.wait_for(client_reader.read(1000), timeout=10.0)

    message = data.decode()
    address = client_writer.get_extra_info('peername')
    print("Received {} from {}".format(message, address))

    # schedule the write operation and flush the buffer
    yield from client_writer.drain()

    print("Close the client socket")
    client_writer.close()


class SimpleTorrentServer:
    def __init__(self, host='127.0.0.1', port=2991):
        self.host = host
        self.port = port

    def fulfill(self):
        loop = asyncio.get_event_loop()
        f = asyncio.start_server(handle_client, host=self.host, port=self.port, loop=loop)
        run_server = loop.run_until_complete(f)

        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(run_server.sockets[0].getsockname()))

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('\nServer stopped')
        finally:
            # Close the server
            run_server.close()
            loop.run_until_complete(run_server.wait_closed())
            loop.close()
