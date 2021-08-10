#!/usr/bin/python3

import random
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from queue import Queue, PriorityQueue

random.seed(42)

# SYSTEM CONSTANTS
LOAD = 0.85
SERVICE = 10.0 # av service time
ARRIVAL = SERVICE/LOAD # av inter-arrival time
TYPE1 = 1 

# SYSTEM PARAMS 
BUFFER_SIZE = float('inf')
FOG_NODES = 5 # number of fog nodes

# SIMULATION PARAMS
SIM_TIME = 500000

# SIMULATION CONSTANTS
arrivals = 0
users = 0
#BusyServer = False # True: server is currently busy; False: server is currently idle
MM1 = [] # clients queue
# True: server is currently idle; False: server is currently busy
FreeFogNodes = [True for fogNode in range(FOG_NODES)]
# Extract costs as gaussian values between zero and one
FogNodesCosts = [np.clip(np.random.normal(0.5, 0.2), 0, 1) for fogNode in range(FOG_NODES)]

class Measure:
    def __init__(self, Narr, Ndep, NAveraegUser, OldTimeEvent, AverageDelay, 
                 ToCloud, NlocallyPreprocessed, ServTime, QueueingDelay, WaitingDelay,
                 BusyTime):
        self.arr = Narr # number of arrivals
        self.dep = Ndep # number of departures
        self.ut = NAveraegUser
        self.oldT = OldTimeEvent
        self.delay = AverageDelay 
        # new metrics
        self.toCloud = ToCloud # pkts sent to cloud
        self.locallyPreprocessed = NlocallyPreprocessed # pkts sent to cloud
        self.serviceTime = ServTime
        self.queueingDelay = QueueingDelay
        self.waitingDelay = WaitingDelay
        
class Client:
    def __init__(self,type,arrival_time,service_time):
        self.type = type
        self.arrival_time = arrival_time
        self.service_time = service_time

class Server(object):
    # constructor
    def __init__(self):
        # whether the server is idle or not
        self.idle = True

# Fog node assignment policies
def RandomAssignFog(FreeFogNodes):
    free_indices = np.where(FreeFogNodes)[0]
    newBusyFogIndex = np.random.choice(free_indices, 1)
    FreeFogNodes[newBusyFogIndex] = False
    return newBusyFogIndex, FreeFogNodes

def RoundRobinAssignFog(FreeFogNodes):
    for fogNode in range(len(FreeFogNodes)):
        if FreeFogNodes[fogNode] == True:
            FreeFogNodes[fogNode] = False
            return fogNode, FreeFogNodes

def LeastCostlyAssignFog(FreeFogNodes, costs):
    free_indices = np.where(FreeFogNodes)[0]
    minCost = np.argmin(np.array(costs)[free_indices])
    newBusyFogIndex = free_indices[minCost]
    FreeFogNodes[newBusyFogIndex] = False
    return newBusyFogIndex, FreeFogNodes

# Event handling functions
def arrival(time, FES, queue):
    global users
    
    #print("Arrival no. ",data.arr+1," at time ",time," with ",users," users" )
    
    # cumulate statistics
    data.arr += 1
    data.ut += users*(time-data.oldT)
    data.oldT = time

    # sample the time until the next event
    inter_arrival = random.expovariate(lambd=1.0/ARRIVAL)
    
    # schedule the next arrival
    FES.put((time + inter_arrival, "arrival"))

    users += 1
    
    # create a record for the client
    client = Client(TYPE1,time,0)

    # insert the record in the queue
    queue.append(client)

    # if the server is idle start the service
    if users <= FOG_NODES:
        # sample the service time
        service_time = random.expovariate(1.0/SERVICE)
        #service_time = 1 + random.uniform(0, SEVICE_TIME)

        # schedule when the client will finish the server
        FES.put((time + service_time, "departure"))
        data.serviceTime += service_time
        client.service_time = service_time
        
    elif users > BUFFER_SIZE + FOG_NODES:
        # if buffer is full send pkt to cloud
        data.toCloud += 1
        # remove client from queue
        users -= 1
        queue.pop(-1)

def departure(time, FES, queue):
    global users

    #print("Departure no. ",data.dep+1," at time ",time," with ",users," users" )
    
    # cumulate statistics
    data.dep += 1
    data.ut += users * (time - data.oldT)
    data.oldT = time
    data.locallyPreprocessed += 1
    
    # get the first element from the queue
    client = queue.pop(0)
    
    # do whatever we need to do when clients go away
    data.delay += (time - client.arrival_time)
    data.queueingDelay.append(time - client.arrival_time)
    users -= 1
        
    # see whether there are more clients to in the line
    if users > FOG_NODES - 1:
        # sample the service time
        service_time = random.expovariate(1.0/SERVICE)

        # schedule when the client will finish the server
        FES.put((time + service_time, "departure"))
        data.serviceTime += service_time
        
        next_client = queue[FOG_NODES - 1]
        next_client.service_time = service_time
        data.waitingDelay.append(time - next_client.arrival_time)


if __name__ == '__main__':
    
    data = Measure(0,0,0,0,0,0,0,0,[],[],0)
    
    # simulation time 
    time = 0
    
    # the list of events in the form: (time, type)
    FES = PriorityQueue()
    
    # schedule the first arrival at t=0
    FES.put((0, "arrival"))
    
    # simulate until the simulated time reaches a constant
    while time < SIM_TIME:
        (time, event_type) = FES.get()
    
        if event_type == "arrival":
            arrival(time, FES, MM1)
    
        elif event_type == "departure":
            departure(time, FES, MM1)
    
    # print output data
    print('MEASUREMENTS')
    print('-'*40)
    print("No. of users in the queue:", users)
    print("No. of arrivals =", data.arr)
    print("No. of departures =", data.dep)
    print("Load:", SERVICE/ARRIVAL)
    print()
    print("Arrival rate:", data.arr/time)
    print("Departure rate:", data.dep/time)
    print()
    print("Average number of users:",data.ut/time)
    print("Average delay:", data.delay/data.dep)
    print("Actual queue size:",len(MM1))
    print("Average service time:", data.serviceTime/data.dep)
    print()
    print("(1) Number of locally pre-processed packets:", data.locallyPreprocessed)
    print("(2) Number of pre-processing forwarded packets:", data.toCloud)
    print("(3) Average number of packets in the system:", data.ut/time)
    print("(4) Average queueing delay:", data.delay/data.dep)
    
    # Distribution of queueing delay
    fig,ax = plt.subplots(1,1)
    sns.distplot(data.queueingDelay, hist=False)
    #ax.hist(data.queueingDelay, bins=500)
    ax.set_title("Distribution of queueing delay")
    ax.set_xlabel('queueing delay')
    ax.set_ylabel('packets')
    plt.show()

    if len(data.waitingDelay) > 0:
        print("(5.a) Average waiting delay over all packets:",
              sum(data.waitingDelay)/data.dep)
        print("(5.b) Average waiting delay over packets that experience delay:", 
              sum(data.waitingDelay)/len(data.waitingDelay))
    
    print("(6) Average buffer occupancy:", data.ut/time)
    print("(7) Pre-processing forward probability:", data.toCloud/data.arr)
    print("(8) Busy time:", data.serviceTime)

    if len(MM1)>0:
        print()
        print("Arrival time of the last element in the queue:",
              MM1[len(MM1)-1].arrival_time)
    
