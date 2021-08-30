'''
Queueing system simmulator class
'''

import random
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from queue import PriorityQueue

random.seed(42)
np.random.seed(42)

class Measure:
    def __init__(self, Narr=0, Ndep=0, NAveraegUser=0, OldTimeEvent=0, AverageDelay=0, 
                 bufferOccupancy=0, oldTbuffer=0, ToCloud=0, NlocallyPreprocessed=0, 
                 ServTime=0, QueueingDelay=[], WaitingDelay=[], departureTimes=[],
                 timeSystem=[], arrivalTimes=[], lossTimes=[], costs=[],
                 lostPktTypes=[], typeAdelay=[], typeBdelay=[], typeAarrival=[],
                 typeBarrival=[]):
        
        self.arr = Narr # number of arrivals
        self.dep = Ndep # number of departures
        self.ut = NAveraegUser
        self.oldT = OldTimeEvent
        self.delay = AverageDelay 
        # new metrics
        self.bufferOccupancy = bufferOccupancy
        self.oldTbuffer = oldTbuffer
        self.toCloud = ToCloud # pkts sent to cloud
        self.locallyPreprocessed = NlocallyPreprocessed # pkts sent to cloud
        self.serviceTime = ServTime
        self.queueingDelay = QueueingDelay
        self.waitingDelay = WaitingDelay
        self.departureTimes = departureTimes
        self.timeSystem = timeSystem
        self.arrivalTimes = arrivalTimes
        self.lossTimes = lossTimes
        self.costs = costs
        self.lostPktTypes = lostPktTypes
        self.typeAdelay = typeAdelay
        self.typeAarrival = typeAarrival
        self.typeBdelay = typeBdelay
        self.typeBarrival = typeBarrival
        

class Client:
    def __init__(self,type,arrival_time,service_time,fogNode,isPreProcessed,cloudServer=False,service_time_cloud=0, arrival_time_cloud=0):
        self.type = type
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.fogNode = fogNode
        self.isPreProcessed = isPreProcessed
        self.cloudServer= cloudServer
        self.service_time_cloud= service_time_cloud
        self.arrival_time_cloud= arrival_time_cloud

class Server(object):
    # constructor
    def __init__(self):
        # whether the server is idle or not
        self.idle = True

# define functions for daily simulation
def dailySimFunctions(plot = False):
    # define interest points
    f_x_points = np.array([0,5,10,12,18,20,24.5]) * 3600000
    f_y_points = [0.8,0.6,0.2,0.4,0.25,0.45,0.8]
    # interpolate points
    f_av_arrival = interp1d(f_x_points, f_y_points, kind='quadratic')
    x = [*range(0, 86400000, 1000)]
    y = f_av_arrival(x) # f(x) is the inter-arrival variation in a day

    if plot:
        x = np.array(x) / 3600000
        f_x_points = np.array(f_x_points) / 3600000
        # Plot inter-arrival variation factor
        plt.plot(f_x_points, f_y_points,'o')
        plt.plot(x, y)
        plt.xlim([0,24])
        plt.ylim([0,1])
        plt.grid()
        plt.xticks(np.arange(0, 25, 2))
        plt.xlabel('time [hours]')
        plt.ylabel('Average inter-arrival time factor [ms]')
        plt.title('Inter-Arrival time variation during the day')
        plt.show()
    
    # define interest points
    f_x_points = np.array([0,2,4,11,13,15,18,20,24.5]) * 3600000
    f_y_points = [0.1,0.05,0.2,0.85,0.85,0.7,0.6,0.5,0.1]
    # interpolate points
    f_f = interp1d(f_x_points, f_y_points, kind='quadratic')
    x = [*range(0, 86400000, 1000)]
    y = f_f(x) # f(x) is the inter-arrival variation in a day

    if plot:
        x = np.array(x) / 3600000
        f_x_points = np.array(f_x_points) / 3600000
        # Plot f variation factor
        plt.plot(f_x_points, f_y_points, 'o')
        plt.plot(x, y)
        plt.xlim([0,24])
        plt.ylim([0,1])
        plt.grid()
        plt.xticks(np.arange(0, 25, 2))
        plt.xlabel('time [hours]')
        plt.ylabel('Ratio of Type B (video pkt)')
        plt.title('Ratio of Tpye B packets')
        plt.show()

    return f_av_arrival, f_f

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

class Simulator():
    def __init__(self, data, data_cloud, LOAD = 0.85, SERVICE = 10.0, ARRIVAL = 0, 
                 BUFFER_SIZE = 3, FOG_NODES = 5, SIM_TIME = 500000, f=0.7, 
                 CLOUD_SERVERS=5, CLOUD_BUFFER_SIZE=3, SERVICE_CLOUD=5, 
                 f_int_arr = None, f_f = None):
        
        # SYSTEM CONSTANTS
        self.LOAD = LOAD
        self.SERVICE = SERVICE
        self.ARRIVAL = ARRIVAL
        self.ARRIVAL_CONST = ARRIVAL
        self.f = f 
        self.SERVICE_CLOUD=SERVICE_CLOUD
        self.prop_delay= 2
        
        # TIME-VARYING FUNCTIONS
        self.f_int_arr = f_int_arr
        self.f_f = f_f
        
        # SYSTEM PARAMS 
        self.BUFFER_SIZE = BUFFER_SIZE
        self.FOG_NODES = FOG_NODES
        self.CLOUD_BUFFER_SIZE = CLOUD_BUFFER_SIZE
        self.CLOUD_SERVERS= CLOUD_SERVERS
        
        # SIMULATION PARAMS
        self.SIM_TIME = SIM_TIME
        
        # SIMULATION CONSTANTS
        self.arrivals = 0
        self.users = 0
        self.users_in_buffer = 0
        self.MM1 = [] # clients queue

        self.users_cloud = 0
        self.users_in_buffer_cloud = 0
        self.MM1_cloud=[]
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

        # CLOUD SERVERS
        # True: server is currently idle; False: server is currently busy
        self.FreeCloudServers = [True for server in range(self.CLOUD_SERVERS)]
        # Busy time for each fog node
        self.CloudServerBusyTime = np.zeros(self.CLOUD_SERVERS)
        # Average service time for each fogNode
        #var = 5
        #self.CloudServerServTime = [np.clip(np.random.normal(SERVICE_CLOUD, var), SERVICE_CLOUD-var, SERVICE_CLOUD+var) for server in range(CLOUD_SERVERS)]
        self.CloudServerServTime = [self.SERVICE_CLOUD for server in range(self.CLOUD_SERVERS)]
        # Cost is inversely proportional to service time i.e. faster node --> more expensive
        self.CloudServerCosts = np.divide(1, self.CloudServerServTime)
        # Extract costs as gaussian values between zero and one
        self.RRindex_cloud = 0 # needed for Round Robin Assignment
        
        # STORE DATA
        self.data = data
        self.data_cloud = data_cloud

    # Event handling functions
    def arrival(self, time, FES, queue, queue_cloud, fog_assign = 'Sorted', 
                distribution = 'Exponential'):
        
        #print("Arrival no. ",data.arr+1," at time ",time," with ",users," users" )
        
        # cumulate statistics
        self.data.arr += 1
        self.data.ut += self.users*(time - self.data.oldT)
        self.data.oldT = time
        self.data.arrivalTimes.append(time)
    
        # sample the time until the next event
        inter_arrival = random.expovariate(lambd=1.0/self.ARRIVAL)
        
        # schedule the next arrival
        self.FES.put((time + inter_arrival, "arrival"))
        self.users += 1
            
        # create a record for the client
        num = random.uniform(0,1) #extract type of packet at random
        if num > self.f:
            pkt_type = 'A'
        else:
            pkt_type = 'B'
        
        client = Client(pkt_type,time,0,None,False,False,0,0)
    
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
            elif distribution == 'Uniform':
                var = 1000
                service_time = fogService + random.uniform(0, var)
            elif distribution == 'Constant':
                service_time = fogService
            
            # schedule when the client will finish the server
            client.isPreProcessed=True
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
            self.FES.put((time+ self.prop_delay, "arrival_cloud"))
            # if buffer is full send pkt to cloud
            self.data.toCloud += 1
            # remove client from queue
            self.users -= 1
            client_cloud=queue.pop(-1)
            client.arrival_time_cloud=time+ self.prop_delay
            queue_cloud.append(client_cloud)

    
    def departure(self, time, FES, queue, queue_cloud, fog_assign = 'Sorted',
                  distribution = 'Exponential'):
    
        #print("Departure no. ",data.dep+1," at time ",time," with ",users," users" )
        
        # cumulate statistics
        self.data.dep += 1
        self.data.ut += self.users * (time - self.data.oldT)
        self.data.oldT = time
        self.data.locallyPreprocessed += 1
        
        # get the first element from the queue
        client = queue.pop(0)
        if client.type == 'B':
            self.FES.put((time+ self.prop_delay, "arrival_cloud"))
            client.arrival_time_cloud=time+ self.prop_delay
            queue_cloud.append(client)
        # do whatever we need to do when clients go away
        self.data.delay += (time - client.arrival_time)
        self.data.queueingDelay.append(time - client.arrival_time)
        self.users -= 1
        if client.type == 'A':
            self.data_cloud.typeAdelay.append(time - client.arrival_time)
            self.data_cloud.typeAarrival.append(client.arrival_time)
        
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
            elif distribution == 'Uniform':
                var = 1000
                service_time = fogService + random.uniform(0, var)
            elif distribution == 'Constant':
                service_time = fogService
    
            # schedule when the client will finish the server
            next_client.isPreProcessed=True
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

    def arrival_cloud(self, time, FES, queue_cloud, server_assign = 'Sorted', 
                distribution = 'Exponential'):
        
        #print("Arrival no. ",data.arr+1," at time ",time," with ",users," users" )
        
        # cumulate statistics
        self.data_cloud.arr += 1
        self.data_cloud.ut += self.users_cloud*(time - self.data_cloud.oldT)
        self.data_cloud.oldT = time
        self.users_cloud += 1
        
        # if the server is idle start the service
        if self.users_cloud <= self.CLOUD_SERVERS:
            client = queue_cloud[self.users_cloud-1]
            # Assign a fogNode to process client
            if server_assign == 'Sorted':
                newBusyServerIndex, self.FreeCloudServers = SortedAssignFog(self.FreeCloudServers)
            elif server_assign == 'RandomAssign':
                newBusyServerIndex, self.FreeCloudServers = RandomAssignFog(self.FreeCloudServers)
            elif server_assign == 'RoundRobin':
                newBusyServerIndex, self.FreeCloudServers = RoundRobinAssignFog(self.FreeCloudServers, self.RRindex_cloud)
            elif server_assign == 'LeastCostly':
                newBusyServerIndex, self.FreeCloudServers = LeastCostlyAssignFog(self.FreeCloudServers, self.CloudServerCosts)
            client.cloudServer = newBusyServerIndex
            self.RRindex_cloud = newBusyServerIndex
    
            # service time of the selected fog node
            serverService = self.CloudServerServTime[client.cloudServer]
    
            # sample the service time
            if distribution == 'Exponential':
                service_time = random.expovariate(1.0/serverService)
            elif distribution == 'Uniform':
                var = 1000
                service_time = serverService + random.uniform(0, var)
            elif distribution == 'Constant':
                service_time = serverService

            if client.type=='B':
                if client.isPreProcessed==True:
                    service_time=2*service_time
                else:
                    service_time=3*service_time

            # schedule when the client will finish the server
            self.FES.put((time + service_time, "departure_cloud"))
            self.data_cloud.serviceTime += service_time
            client.service_time_cloud = service_time
            # Update busy time 
            self.CloudServerBusyTime[client.cloudServer] += service_time
            self.data_cloud.costs.append(service_time * self.CloudServerCosts[client.cloudServer])
            
        elif self.users_cloud > self.CLOUD_SERVERS and self.users_cloud <= self.CLOUD_BUFFER_SIZE + self.CLOUD_SERVERS:
            # users go into the buffer
            self.data_cloud.bufferOccupancy += self.users_in_buffer_cloud * (time - self.data_cloud.oldTbuffer)
            self.data_cloud.oldTbuffer = time
            self.users_in_buffer_cloud += 1
    
        elif self.users_cloud > self.CLOUD_BUFFER_SIZE + self.CLOUD_SERVERS:
            # if buffer is full drop pkt 
            self.data_cloud.toCloud += 1 #this are dropped packets
            self.data_cloud.lossTimes.append(time)
            # remove client from queue
            self.users_cloud -= 1
            client = queue_cloud.pop(-1)
            self.data_cloud.lostPktTypes.append(client.type)
            

    def departure_cloud(self, time, FES, queue_cloud, server_assign = 'Sorted',
                  distribution = 'Exponential'):
    
        #print("Departure no. ",data.dep+1," at time ",time," with ",users," users" )
        
        # cumulate statistics
        self.data_cloud.dep += 1
        self.data_cloud.ut += self.users_cloud * (time - self.data_cloud.oldT)
        self.data_cloud.oldT = time
        self.data_cloud.locallyPreprocessed += 1
        
        # get the first element from the queue
        client = queue_cloud.pop(0)
        
        # do whatever we need to do when clients go away
        self.data_cloud.delay += (time - client.arrival_time_cloud)
        self.data_cloud.queueingDelay.append(time - client.arrival_time_cloud)
        self.data_cloud.waitingDelay.append(time - client.arrival_time_cloud - client.service_time_cloud)
        self.data_cloud.departureTimes.append(time)
        self.data_cloud.timeSystem.append(time - client.arrival_time)
        self.users_cloud -= 1
        
        if client.type == 'A':
            self.data_cloud.typeAdelay.append(time - client.arrival_time)
            self.data_cloud.typeAarrival.append(client.arrival_time)
        elif client.type == 'B':
            self.data_cloud.typeBdelay.append(time - client.arrival_time)
            self.data_cloud.typeBarrival.append(client.arrival_time)
        
        # free fogNode
        self.FreeCloudServers[client.cloudServer] = True
        
        # see whether there are more clients to in the line
        if self.users_cloud > self.CLOUD_SERVERS - 1:
            # Next client is the first in the queue after the ones in the fog nodes
            next_client = queue_cloud[self.CLOUD_SERVERS - 1]
            
            # Assign a fogNode to process client
            if server_assign == 'Sorted':
                newBusyServerIndex, self.FreeCloudServers = SortedAssignFog(self.FreeCloudServers)
            elif server_assign == 'RandomAssign':
                newBusyServerIndex, self.FreeCloudServers = RandomAssignFog(self.FreeCloudServers)
            elif server_assign == 'RoundRobin':
                newBusyServerIndex, self.FreeCloudServers = RoundRobinAssignFog(self.FreeCloudServers, self.RRindex_cloud)
            elif server_assign == 'LeastCostly':
                newBusyServerIndex, self.FreeCloudServers = LeastCostlyAssignFog(self.FreeCloudServers, self.CloudServerCosts)
            next_client.cloudServer = newBusyServerIndex
            self.RRindex_cloud = newBusyServerIndex
    
            # service time of the selected fog node
            serverService = self.CloudServerServTime[next_client.cloudServer]
    
            # sample the service time
            if distribution == 'Exponential':
                service_time = random.expovariate(1.0/serverService)
            elif distribution == 'Uniform':
                var = 1000
                service_time = serverService + random.uniform(0, var)
            elif distribution == 'Constant':
                service_time = serverService

            if next_client.type == 'B':
                if next_client.isPreProcessed == True:
                    service_time = 2 * service_time
                else:
                    service_time = 3 * service_time

            # schedule when the client will finish the server
            self.FES.put((time + service_time, "departure_cloud"))
            self.data_cloud.serviceTime += service_time
            
            # Update stats
            next_client.service_time_cloud = service_time
            #self.data_cloud.waitingDelay.append(time - next_client.arrival_time_cloud)
            self.CloudServerBusyTime[next_client.cloudServer] += service_time
            self.data_cloud.costs.append(service_time * self.CloudServerCosts[next_client.cloudServer])
            
            # update buffer counter
            self.data_cloud.bufferOccupancy += self.users_in_buffer_cloud * (time - self.data_cloud.oldTbuffer)
            self.data_cloud.oldTbuffer = time
            self.users_in_buffer_cloud -= 1
            
    def simulate(self, print_everything = True, fog_assign = 'Sorted',
                 distribution = 'Exponential'):
        
        # simulation time
        time = 0
        
        # schedule the first arrival at t=0
        self.FES.put((0, "arrival"))
        
        # simulate until the simulated time reaches a constant
        while time < self.SIM_TIME:
            
            (time, event_type) = self.FES.get()
            
            if self.f_int_arr:
                self.ARRIVAL = float(self.ARRIVAL_CONST * self.f_int_arr(time))
            if self.f_f:
                self.f = float(self.f_f(time))
        
            if event_type == "arrival":
                self.arrival(time, self.FES, self.MM1, self.MM1_cloud, fog_assign, distribution)
        
            elif event_type == "departure":
                self.departure(time, self.FES, self.MM1, self.MM1_cloud, fog_assign, distribution)

            elif event_type == "arrival_cloud":
                self.arrival_cloud(time, self.FES, self.MM1_cloud, fog_assign, distribution)

            elif event_type == "departure_cloud":
                self.departure_cloud(time, self.FES, self.MM1_cloud, fog_assign, distribution)
        
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
            
        return self.data, self.data_cloud, time, self.FogBusyTime, sum(self.FogBusyTime * self.FogNodesCosts)
    

if __name__ == '__main__':
    
    data = Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                   [],[],[],[],[],[],[],[],[])
    data_cloud = Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                         [],[],[],[],[],[],[],[],[])
    
    LOAD = 0.85
    SERVICE = 10.0
    ARRIVAL = SERVICE/LOAD # default arrival
    
    # SYSTEM PARAMS 
    BUFFER_SIZE = 3 #float('inf')
    FOG_NODES = 5 # number of fog nodes
    
    #CLOUD PARAMETERS
    f=0.7
    CLOUD_SERVERS=5
    CLOUD_BUFFER_SIZE=3
    SERVICE_CLOUD=5

    # SIMULATION PARAMS
    SIM_TIME = 500000

    # instaciate simulator
    s = Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, SERVICE_CLOUD)
    print_everything = True
    data, data_cloud, time, _, _ = s.simulate(print_everything)
    

