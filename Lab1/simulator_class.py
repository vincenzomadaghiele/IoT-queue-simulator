'''
Queueing system simmulator class for lab1
'''

import random
import numpy as np
from matplotlib import pyplot as plt
from queue import PriorityQueue

random.seed(42)
np.random.seed(42)

class Measure:
    def __init__(self, Narr=0, Ndep=0, NAveraegUser=0, OldTimeEvent=0, AverageDelay=0, 
                 bufferOccupancy=0, oldTbuffer=0, ToCloud=0, NlocallyPreprocessed=0, 
                 ServTime=0, QueueingDelay=[], WaitingDelay=[]):
        self.arr = Narr # number of arrivals
        self.dep = Ndep # number of departures
        self.ut = NAveraegUser # average number of users
        self.oldT = OldTimeEvent # last time event
        self.delay = AverageDelay # average delay
        self.bufferOccupancy = bufferOccupancy # buffer occupancy
        self.oldTbuffer = oldTbuffer # last time event in the buffer
        self.toCloud = ToCloud # pkts sent to cloud
        self.locallyPreprocessed = NlocallyPreprocessed # pkts sent to cloud
        self.serviceTime = ServTime # service time
        self.queueingDelay = QueueingDelay # queueing delay
        self.waitingDelay = WaitingDelay # waiting delay

class Client:
    def __init__(self,type,arrival_time,service_time,fogNode):
        self.type = type
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.fogNode = fogNode

# Fog node assignment policies
def SortedAssignFog(FreeFogNodes):
    for fogNode in range(len(FreeFogNodes)):
        if FreeFogNodes[fogNode] == True:
            FreeFogNodes[fogNode] = False
            return fogNode, FreeFogNodes

def RandomAssignFog(FreeFogNodes):
    free_indices = np.where(FreeFogNodes)[0]
    newBusyFogIndex = np.random.choice(free_indices)
    FreeFogNodes[newBusyFogIndex] = False
    return newBusyFogIndex, FreeFogNodes

def RoundRobinAssignFog(FreeFogNodes, startingNode):
    shifted_indices = np.roll(np.array(range(len(FreeFogNodes))),-(startingNode+1))
    for fogNode in shifted_indices:
        if FreeFogNodes[fogNode] == True:
            FreeFogNodes[fogNode] = False
            return fogNode, FreeFogNodes

def LeastCostlyAssignFog(FreeFogNodes, costs):
    free_indices = np.where(FreeFogNodes)[0]
    minCost = np.argmin(np.array(costs)[free_indices])
    newBusyFogIndex = free_indices[minCost]
    FreeFogNodes[newBusyFogIndex] = False
    return newBusyFogIndex, FreeFogNodes

# Simulator class
class Simulator():
    def __init__(self, data, LOAD = 0.85, SERVICE = 10.0, ARRIVAL = 0,
                 BUFFER_SIZE = 3, FOG_NODES = 5, SIM_TIME = 500000):
        
        # SYSTEM CONSTANTS
        self.LOAD = LOAD
        self.SERVICE = SERVICE
        self.ARRIVAL = ARRIVAL
        self.TYPE1 = 1
        
        # SYSTEM PARAMS 
        self.BUFFER_SIZE = BUFFER_SIZE
        self.FOG_NODES = FOG_NODES
        
        # SIMULATION PARAMS
        self.SIM_TIME = SIM_TIME
        
        # SIMULATION CONSTANTS
        self.arrivals = 0
        self.users = 0
        self.users_in_buffer = 0
        self.MM1 = [] # clients queue
        # the list of events in the form: (time, type)
        self.FES = PriorityQueue()

        # FOG NODES
        # True: server is currently idle; False: server is currently busy
        self.FreeFogNodes = [True for fogNode in range(self.FOG_NODES)]
        # Busy time for each fog node
        self.FogBusyTime = np.zeros(self.FOG_NODES)
        # Average service time for each fogNode
        #var = 5
        #self.FogNodesServTime = [np.clip(np.random.normal(SERVICE, var), SERVICE-var, SERVICE+var) for fogNode in range(FOG_NODES)]
        self.FogNodesServTime = [self.SERVICE for fogNode in range(self.FOG_NODES)]
        # Cost is inversely proportional to service time i.e. faster node --> more expensive
        self.FogNodesCosts = np.divide(1, self.FogNodesServTime)
        # Extract costs as gaussian values between zero and one
        self.RRindex = 0 # needed for Round Robin Assignment
        
        # STORE DATA
        self.data = data

    # Event handling functions
    def arrival(self, time, FES, queue, fog_assign = 'Sorted', 
                distribution = 'Exponential'):
        
        #print("Arrival no. ",data.arr+1," at time ",time," with ",users," users" )
        
        # cumulate statistics
        self.data.arr += 1
        self.data.ut += self.users*(time - self.data.oldT)
        self.data.oldT = time
    
        # sample the time until the next event
        inter_arrival = random.expovariate(lambd=1.0/self.ARRIVAL)
        
        # schedule the next arrival
        self.FES.put((time + inter_arrival, "arrival"))
    
        self.users += 1
            
        # create a record for the client
        client = Client(self.TYPE1,time,0,None)
    
        # insert the record in the queue
        queue.append(client)
    
        # if the server is idle start the service
        if self.users <= self.FOG_NODES:
            # Assign a fogNode to process client
            if fog_assign == 'Sorted':
                newBusyFogIndex, self.FreeFogNodes = SortedAssignFog(self.FreeFogNodes)
            elif fog_assign == 'RandomAssign':
                newBusyFogIndex, self.FreeFogNodes = RandomAssignFog(self.FreeFogNodes)
            elif fog_assign == 'RoundRobin':
                newBusyFogIndex, self.FreeFogNodes = RoundRobinAssignFog(self.FreeFogNodes, self.RRindex)
            elif fog_assign == 'LeastCostly':
                newBusyFogIndex, self.FreeFogNodes = LeastCostlyAssignFog(self.FreeFogNodes, self.FogNodesCosts)
            client.fogNode = newBusyFogIndex
            self.RRindex = newBusyFogIndex
    
            # service time of the selected fog node
            fogService = self.FogNodesServTime[client.fogNode]
    
            # sample the service time
            if distribution == 'Exponential':
                service_time = random.expovariate(1.0/fogService)
            elif distribution == 'Constant':
                service_time = fogService
            elif distribution == 'Uniform':
                var = 200
                service_time=random.uniform(fogService-(var/2), fogService+(var/2))
            
            # schedule when the client will finish the server
            self.FES.put((time + service_time, "departure"))
            self.data.serviceTime += service_time
            client.service_time = service_time
            # Update busy time 
            self.FogBusyTime[client.fogNode] += client.service_time
            
        elif self.users > self.FOG_NODES and self.users <= self.BUFFER_SIZE + self.FOG_NODES:
            # users go into the buffer
            self.data.bufferOccupancy += self.users_in_buffer * (time - self.data.oldTbuffer)
            self.data.oldTbuffer = time
            self.users_in_buffer += 1
    
        elif self.users > self.BUFFER_SIZE + self.FOG_NODES:
            # if buffer is full send pkt to cloud
            self.data.toCloud += 1
            # remove client from queue
            self.users -= 1
            queue.pop(-1)
    
    def departure(self, time, FES, queue, fog_assign = 'Sorted',
                  distribution = 'Exponential'):
    
        #print("Departure no. ",data.dep+1," at time ",time," with ",users," users" )
        
        # cumulate statistics
        self.data.dep += 1
        self.data.ut += self.users * (time - self.data.oldT)
        self.data.oldT = time
        self.data.locallyPreprocessed += 1
        
        # get the first element from the queue
        client = queue.pop(0)
        
        # do whatever we need to do when clients go away
        self.data.delay += (time - client.arrival_time)
        self.data.queueingDelay.append(time - client.arrival_time)
        self.users -= 1
        
        # free fogNode
        self.FreeFogNodes[client.fogNode] = True
        
        # see whether there are more clients to in the line
        if self.users > self.FOG_NODES - 1:
            # Next client is the first in the queue after the ones in the fog nodes
            next_client = queue[self.FOG_NODES - 1]
            
            # Assign a fogNode to process client
            if fog_assign == 'Sorted':
                newBusyFogIndex, self.FreeFogNodes = SortedAssignFog(self.FreeFogNodes)
            elif fog_assign == 'RandomAssign':
                newBusyFogIndex, self.FreeFogNodes = RandomAssignFog(self.FreeFogNodes)
            elif fog_assign == 'RoundRobin':
                newBusyFogIndex, self.FreeFogNodes = RoundRobinAssignFog(self.FreeFogNodes, self.RRindex)
            elif fog_assign == 'LeastCostly':
                newBusyFogIndex, self.FreeFogNodes = LeastCostlyAssignFog(self.FreeFogNodes, self.FogNodesCosts)
            next_client.fogNode = newBusyFogIndex
            self.RRindex = newBusyFogIndex
    
            # service time of the selected fog node
            fogService = self.FogNodesServTime[client.fogNode]
    
            # sample the service time
            if distribution == 'Exponential':
                service_time = random.expovariate(1.0/fogService)
            elif distribution == 'Constant':
                service_time = fogService
            elif distribution == 'Uniform':
                var = 200
                service_time=random.uniform(fogService-(var/2), fogService+(var/2))
            
    
            # schedule when the client will finish the server
            self.FES.put((time + service_time, "departure"))
            self.data.serviceTime += service_time
            
            # Update stats
            next_client.service_time = service_time
            self.data.waitingDelay.append(time - next_client.arrival_time)
            self.FogBusyTime[next_client.fogNode] += next_client.service_time
            
            # update buffer counter
            self.data.bufferOccupancy += self.users_in_buffer * (time - self.data.oldTbuffer)
            self.data.oldTbuffer = time
            self.users_in_buffer -= 1
            
    def simulate(self, print_everything = True, fog_assign = 'Sorted',
                 distribution = 'Exponential'):
        
        # simulation time
        time = 0
        
        # schedule the first arrival at t=0
        self.FES.put((0, "arrival"))
        
        # simulate until the simulated time reaches a constant
        while time < self.SIM_TIME:
            (time, event_type) = self.FES.get()
        
            if event_type == "arrival":
                self.arrival(time, self.FES, self.MM1, fog_assign, distribution)
        
            elif event_type == "departure":
                self.departure(time, self.FES, self.MM1, fog_assign, distribution)
        
        if print_everything:
            # print output data
            print('MEASUREMENTS')
            print('-'*40)
            print("No. of users in the queue:", self.users)
            print("No. of arrivals =", self.data.arr)
            print("No. of departures =", self.data.dep)
            print("Load:", self.SERVICE/self.ARRIVAL)
            print("Node assigment method:", fog_assign)
            print("Distribution of service time:", distribution)
            print()
            print("Arrival rate:", self.data.arr/time)
            print("Departure rate:", self.data.dep/time)
            print("Actual queue size:",len(self.MM1))
            print("Average service time:", self.data.serviceTime/self.data.dep)
            print()
            print("(1) Number of locally pre-processed packets:", self.data.locallyPreprocessed)
            print("(2) Number of pre-processing forwarded packets:", self.data.toCloud)
            print("(3) Average number of packets in the system:", self.data.ut/time)
            print("(4) Average queueing delay:", self.data.delay/self.data.dep)
            
            # Distribution of queueing delay
            fig,ax = plt.subplots(1,1)
            #sns.distplot(data.queueingDelay, hist=False)
            ax.hist(self.data.queueingDelay, bins=500)
            ax.set_title("Distribution of queueing delay")
            ax.set_xlabel('queueing delay')
            ax.set_ylabel('packets')
            plt.show()
        
            if len(self.data.waitingDelay) > 0:
                print("(5.a) Average waiting delay over all packets:",
                      sum(self.data.waitingDelay)/self.data.dep)
                print("(5.b) Average waiting delay over packets that experience delay:", 
                      sum(self.data.waitingDelay)/len(self.data.waitingDelay))
            else:
                print("(5.a) Average waiting delay: None")
        
            print("(6) Average buffer occupancy:", self.data.bufferOccupancy/time)
            print("(7) Pre-processing forward probability:", self.data.toCloud/self.data.arr)
            print("(8) Busy time:", self.data.serviceTime)
            print('(9) Total operational costs:', sum(self.FogBusyTime * self.FogNodesCosts))
        
            if len(self.MM1)>0:
                print()
                print("Arrival time of the last element in the queue:",
                      self.MM1[len(self.MM1)-1].arrival_time)
            print()
            
        return self.data, time, self.FogBusyTime, sum(self.FogBusyTime * self.FogNodesCosts)
    

if __name__ == '__main__':
    
    data = Measure(0,0,0,0,0,0,0,0,0,0,[],[])
    
    LOAD = 0.85
    SERVICE = 10.0
    ARRIVAL = SERVICE/LOAD # default arrival
    
    # SYSTEM PARAMS 
    BUFFER_SIZE = 3 #float('inf')
    FOG_NODES = 5 # number of fog nodes
    
    # SIMULATION PARAMS
    SIM_TIME = 500000

    # instaciate simulator
    s = Simulator(data, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, FOG_NODES, SIM_TIME)
    print_everything = True
    data, time, _, _ = s.simulate(print_everything)
    

