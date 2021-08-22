'''
Exercise 4b
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
    s.CloudServerServTime = [200, 500, 500, 1000]
    s.CloudServerCosts = [1, 0.4, 0.4, 0.1]
    
    print_everything = False
    data, data_cloud, time, _, _ = s.simulate(print_everything)
    
    print('A-B-B-C simulation')
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


    # AABC
    # data storage object
    data = sim.Measure()
    data_cloud = sim.Measure()
    
    # simulator
    s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s.CloudServerServTime = [100, 100, 500, 1000]
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
    
    costs_hourlyAABC = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloud.departureTimes)):
            if data_cloud.departureTimes[j] > i * 3600000 and data_cloud.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloud.costs[j]
        costs_hourlyAABC.append(cost_hourly)


    # ABCC
    # data storage object
    data = sim.Measure()
    data_cloud = sim.Measure()
    
    # simulator
    s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s.CloudServerServTime = [100, 500, 1000, 1000]
    s.CloudServerCosts = [1, 0.4, 0.1, 0.1]
    
    print_everything = False
    data, data_cloud, time, _, _ = s.simulate(print_everything)
    
    print('A-B-C-C simulation')
    print('-'*40)
    print(f'Average Queueing Delay [ms] = {(data.delay + data_cloud.delay) / (data.dep + data_cloud.dep)}')
    print(f'Loss Probability = {data_cloud.toCloud/data.arr}')
    print(f'Average number of users = {(data.ut + data_cloud.ut)/time}')
    print(f'Total Operational Cost = {sum(s.FogBusyTime * s.FogNodesCosts) + sum(s.CloudServerBusyTime * s.CloudServerCosts)}')
    
    
    # Average queueing delay with progressively faster MDC service
    
    costs_hourlyABCC = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloud.departureTimes)):
            if data_cloud.departureTimes[j] > i * 3600000 and data_cloud.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloud.costs[j]
        costs_hourlyABCC.append(cost_hourly)


    #%% BCAA
    
    # data storage object
    data = sim.Measure()
    data_cloud = sim.Measure()
    
    # simulator
    s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s.CloudServerServTime = [500, 1000, 100, 100]
    s.CloudServerCosts = [0.4, 0.1, 1, 1]
    
    print_everything = False
    data, data_cloud, time, _, _ = s.simulate(print_everything)
    
    print('B-C-A-A simulation')
    print('-'*40)
    print(f'Average Queueing Delay [ms] = {(data.delay + data_cloud.delay) / (data.dep + data_cloud.dep)}')
    print(f'Loss Probability = {data_cloud.toCloud/data.arr}')
    print(f'Average number of users = {(data.ut + data_cloud.ut)/time}')
    print(f'Total Operational Cost = {sum(s.FogBusyTime * s.FogNodesCosts) + sum(s.CloudServerBusyTime * s.CloudServerCosts)}')
    

    costs_hourlyBCAA = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloud.departureTimes)):
            if data_cloud.departureTimes[j] > i * 3600000 and data_cloud.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloud.costs[j]
        costs_hourlyBCAA.append(cost_hourly)
    
    
    #%% Average queueing delay with progressively faster MDC service

    plt.grid(axis='y',zorder=0)
    plt.bar([*range(0,24)],costs_hourlyABBC, zorder=3)
    plt.xticks(np.arange(0, 25, 2))
    plt.xlabel("time [hours]")
    plt.ylabel("Cost")
    plt.title('Hourly cost of the cloud server')
    plt.show()

    fig, ax = plt.subplots(figsize=(14, 5))
    x = np.array([*range(0,24)])
    ax = plt.subplot()
    w = 0.3
    plt.grid(axis='y',zorder=0)
    ax.bar(x, costs_hourlyAABC, width=w, align='center', zorder=3, label='A-A-B-C')
    ax.bar(x-w, costs_hourlyABBC, width=w, align='center', zorder=3, label='A-B-B-C')
    ax.bar(x+w, costs_hourlyABCC, width=w, align='center', zorder=3, label='A-B-C-C')
    ax.autoscale(tight=True)
    plt.legend()
    plt.xticks(np.arange(0, 24, 1))
    plt.xlabel("time [hours]")
    plt.ylabel("Cost")
    plt.title('Overall hourly cost of the cloud system')
    plt.show()
    
