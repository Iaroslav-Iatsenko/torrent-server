import os
import math

SPLIT_STEP = 1024

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

@staticmethod            
def file_lenth(file):
    return os.stat(file).st_size

class Filespliter:
    def __init__(self, filename):
      self.filename=filename
      self.filelenth= file_lenth(filename)
      self.total_shards=math.ceil(self.filelenth/SPLIT_STEP)
      self.shards_list={}
      for i in range(self.total_shards):
        self.shards_list[i] = Shard(self.filename, i)
