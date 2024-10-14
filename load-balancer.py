from collections import deque
import sys
from random import randint
import json
from functools import reduce
import operator

import random

def generate_ordered_list(n, start, end):
    # Generate 'n' random unique integers in the range [start, end]
    random_integers = random.sample(range(start, end + 1), n)
    
    # Sort the list to ensure it's ordered
    ordered_list = sorted(random_integers)
    
    return ordered_list

def load_requisition(requision_type, packet_size):
    return {
        "type" : "I/O" if requision_type == 0 else "processing"
        "size" : packet_size
    }

def traffic_simulator(delta_range=1e5):
    MIN_DELTA_SIZE = 1e5 # minimum number of deltas
    MIN_REQ_RANGE, MAX_REQ_RANGE = 1e1,1e4 # requisitons can have 10 to 10000 bytes in size
    MAX_REQS_PER_DELTA = 5 # can have 1 to 5 requisitions:

    deltas = generate_ordered_list(range(1,randint(MIN_DELTA_SIZE,MIN_DELTA_SIZE+delta_range)), 0, MIN_DELTA_SIZE+delta_range)
    traffic = {}
    for delta in deltas:
        reqs = []
        for _ in range(0,MAX_REQS_PER_DELTA): # can have 1 to 5 requisitions:
            reqs.append(load_requisition(randint(0,1), randint(MIN_REQ_RANGE, MAX_REQ_RANGE)) ) # req can be I/O or processing
        traffic[delta] = reqs
    return traffic

class ServerSimulator:
    delta = 0
    def __init__(self,byte_processing_time):
        self.byte_processing_time = byte_processing_time
        self.queue = deque()
        self.load_receive_time = 0
        self.load_
    
    def receive_load(self,load):
        self.load_receive_time = delta
        self.queue.append(load)
    
    def process_load(self):
        # verifica se fila tem algo e se uma load foi processada.
        if self.queue and delta - self.load_receive_time >= self.byte_processing_time + :
            self.queue.popleft()
            print("finish load time")
            self.load_receive_time = delta
    

class LoadBalancer:
    pass


def TestSimulator:
    def __init__(self,n_deltas,):
        self.n_deltas = n_deltas
    
    def begin_simulation(self,):

        while delta <= 7: # sys.maxint:
            print(ServerSimulator.delta)
            s1.process_load()
            delta += 1
            ServerSimulator.delta = delta
    
    def write_log(self,entry,paths):
        with open('log.json',r+) as f:
            file = json.load(f)
            data = json.loads(file)
            set_in_dict(data,)

    def get_from_dict(dataDict, mapList):
        return reduce(operator.getitem, mapList, dataDict)

    def set_in_dict(dataDict, mapList, value):
        getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value

if __name__ == "__main__":
    
    delta = 0
    s1 = ServerSimulator(randint(1,10))
    s2 = ServerSimulator(3)
    s3 = ServerSimulator(3)
    s1.receive_load(3)
    s1.receive_load(3)
    while delta <= 7: # sys.maxint:
        print(ServerSimulator.delta)
        s1.process_load()
        delta += 1
        ServerSimulator.delta = delta