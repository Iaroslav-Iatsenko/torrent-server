import asyncio
import os
import math

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
        self.loop = asyncio.get_event_loop()
        f = asyncio.start_server(
            handle_client, host=self.host, port=self.port, loop=self.loop
        )
        self.run_server = self.loop.run_until_complete(f)

    def run(self):
        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(self.run_server.sockets[0].getsockname()))

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print('\nServer stopped')
        finally:
            self.stop()

    def stop(self):
        # Close the server
        self.run_server.close()
        self.loop.run_until_complete(self.run_server.wait_closed())
        self.loop.close()
        
class Shard:
    def __init__(self, filename, index, open=open):
        self._index = index
        with open(filename, 'rb') as file:
            file.seek(index * SPLIT_STEP)
            self._data = file.read(SPLIT_STEP)

    def save(self, filename):
        with open(filename, 'wb') as file:
            file.seek(self._index * SPLIT_STEP)
file.write(self._data)        

SPLIT_STEP = 1024
def file_lenth(file):
    return os.stat('somefile.txt').st_size

def filespliter(self, file):
    self.file=file
    self.filelenth= file_lenth(self,file)
    self.total_shards=math.ceil(self.filelenth/SPLIT_STEP)
    self.sherds_list={}
    for i in range(self.total_shards):
        self.sherds_list[i] = Shard(self.file, i)
        

    
    
        
