'''
Exercise 4c
'''

import random
import numpy as np
from matplotlib import pyplot as plt
import simulator_class2 as sim

random.seed(42)
np.random.seed(42)

if __name__ == '__main__':
    
    f_av_arrival, f_f = sim.dailySimFunctions()

    # simulate ABBC
        
    # Micro Data Center (MDC)
    SERVICE = 1000
    ARRIVAL = 500
    LOAD = SERVICE/ARRIVAL
    BUFFER_SIZE = 5
    FOG_NODES = 4
    
    # Cloud Data Center (CDC)
    f = 0.8
    SERVICE_CLOUD = 500
    CLOUD_BUFFER_SIZE = 10
    CLOUD_SERVERS = 4
    
    # SIMULATION PARAMS
    SIM_TIME = 86400000 # 24 hours simulation
    
    # data storage object
    data = sim.Measure()
    data_cloud = sim.Measure()
    
    # simulator
    s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s.CloudServerServTime = [200, 200, 500, 1000]
    s.CloudServerCosts = [1, 1, 0.4, 0.1]
    
    print_everything = False
    data, data_cloud, time, _, _ = s.simulate(print_everything)
    
    print('A-A-B-C simulation')
    print('-'*40)
    print(f'Average Queueing Delay [ms] = {(data.delay + data_cloud.delay) / (data.dep + data_cloud.dep)}')
    print(f'Loss Probability = {data_cloud.toCloud/data.arr}')
    print(f'Average number of users = {(data.ut + data_cloud.ut)/time}')
    print(f'Total Operational Cost = {sum(s.FogBusyTime * s.FogNodesCosts) + sum(s.CloudServerBusyTime * s.CloudServerCosts)}')
    
    
    # Average queueing delay with progressively faster MDC service
    costs_hourlyABBC = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloud.departureTimes)):
            if data_cloud.departureTimes[j] > i * 3600000 and data_cloud.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloud.costs[j]
        costs_hourlyABBC.append(cost_hourly)

    plt.grid(axis='y',zorder=0)
    plt.bar([*range(0,24)],costs_hourlyABBC, zorder=3)
    plt.xticks(np.arange(0, 25, 2))
    plt.xlabel("time [hours]")
    plt.ylabel("Cost")
    plt.title('Hourly cost of the cloud server')
    plt.show()
