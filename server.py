import asyncio
import logging

log = logging.getLogger(__name__)

clients = {}  # task -> (reader, writer)


def server():
    loop = asyncio.get_event_loop()
    f = asyncio.start_server(accept_client, host=None, port=2991)
    loop.run_until_complete(f)
    loop.run_forever()


def accept_client(client_reader, client_writer):
    task = asyncio.Task(handle_client(client_reader, client_writer))
    clients[task] = (client_reader, client_writer)

    def client_done(client_task):
        del clients[client_task]
        client_writer.close()
        log.warning("End Connection")

    log.warning("New Connection")
    task.add_done_callback(client_done)


@asyncio.coroutine
def handle_client(client_reader, client_writer):
    # let the client know they are connected
    client_writer.write("Connection established\n".encode())

    # give client a chance to respond, timeout after 10 seconds
    data = yield from asyncio.wait_for(client_reader.readline(),
                                       timeout=10.0)

    if data is None:
        log.warning("Expected some data, received None")
        return

    some_message = data.decode().rstrip()
    log.warning("Received {}".format(some_message))

    client_writer.write("READY\n".encode())
    while True:
        # wait for input from client
        data = yield from asyncio.wait_for(client_reader.readline(),
                                           timeout=10.0)
        if data is None:
            log.warning("Received no data")
            # exit echo loop and disconnect
            return

        sent_data = data.decode().rstrip()
        if sent_data.upper() == 'BYE':
            client_writer.write("BYE\n".encode())
            break
        response = ("ECHO {}\n".format(sent_data))
        client_writer.write(response.encode())


if __name__ == '__main__':
    server()
