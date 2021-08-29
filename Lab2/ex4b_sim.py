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
        
    
    #%% ABBC
    # data storage object
    dataABBC = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    data_cloudABBC = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    
    # simulator
    s_ABBC = sim.Simulator(dataABBC, data_cloudABBC, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s_ABBC.CloudServerServTime = [200, 500, 500, 1000]
    s_ABBC.CloudServerCosts = [1, 0.4, 0.4, 0.1]
    
    print_everything = False
    dataABBC, data_cloudABBC, time, _, _ = s_ABBC.simulate(print_everything)
    
    print('A-B-B-C simulation')
    print('-'*40)
    print(f'Average Queueing Delay [ms] = {(dataABBC.delay + data_cloudABBC.delay) / (dataABBC.dep + data_cloudABBC.dep)}')
    print(f'Loss Probability = {data_cloudABBC.toCloud/dataABBC.arr}')
    print(f'Average number of users = {(dataABBC.ut + data_cloudABBC.ut)/time}')
    print(f'Total Operational Cost = {sum(s_ABBC.FogBusyTime * s_ABBC.FogNodesCosts) + sum(s_ABBC.CloudServerBusyTime * s_ABBC.CloudServerCosts)}')
    print(f'Micro Data Center Operational Cost = {sum(s_ABBC.FogBusyTime * s_ABBC.FogNodesCosts)}')
    print(f'Cloud Data Center Operational Cost = {sum(s_ABBC.CloudServerBusyTime * s_ABBC.CloudServerCosts)}')
    
    # Average queueing delay with progressively faster MDC service
    costs_hourlyABBC = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloudABBC.departureTimes)):
            if data_cloudABBC.departureTimes[j] > i * 3600000 and data_cloudABBC.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloudABBC.costs[j]
        costs_hourlyABBC.append(cost_hourly)

    delay_hourly_avgsABBC = []
    for i in range(0,24):
        delay_hourly_avg = 0
        hour_count = 0
        for j in range(len(data_cloudABBC.departureTimes)):
            if data_cloudABBC.departureTimes[j] > i * 3600000 and data_cloudABBC.departureTimes[j] < (i+1) * 3600000:
                delay_hourly_avg += data_cloudABBC.timeSystem[j]
                hour_count += 1
        delay_hourly_avg /= hour_count
        delay_hourly_avgsABBC.append(delay_hourly_avg)


    #%% AABC
    # data storage object
    dataAABC = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    data_cloudAABC = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    
    # simulator
    s_AABC = sim.Simulator(dataAABC, data_cloudAABC, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s_AABC.CloudServerServTime = [200, 200, 500, 1000]
    s_AABC.CloudServerCosts = [1, 1, 0.4, 0.1]
    
    print_everything = False
    dataAABC, data_cloudAABC, time, _, _ = s_AABC.simulate(print_everything)
    
    print('A-A-B-C simulation')
    print('-'*40)
    print(f'Average Queueing Delay [ms] = {(dataAABC.delay + data_cloudAABC.delay) / (dataAABC.dep + data_cloudAABC.dep)}')
    print(f'Loss Probability = {data_cloudAABC.toCloud/dataAABC.arr}')
    print(f'Average number of users = {(dataAABC.ut + data_cloudAABC.ut)/time}')
    print(f'Total Operational Cost = {sum(s_AABC.FogBusyTime * s_AABC.FogNodesCosts) + sum(s_AABC.CloudServerBusyTime * s_AABC.CloudServerCosts)}')
    print(f'Micro Data Center Operational Cost = {sum(s_AABC.FogBusyTime * s_AABC.FogNodesCosts)}')
    print(f'Cloud Data Center Operational Cost = {sum(s_AABC.CloudServerBusyTime * s_AABC.CloudServerCosts)}')

    # Average queueing delay with progressively faster MDC service
    costs_hourlyAABC = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloudAABC.departureTimes)):
            if data_cloudAABC.departureTimes[j] > i * 3600000 and data_cloudAABC.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloudAABC.costs[j]
        costs_hourlyAABC.append(cost_hourly)

    delay_hourly_avgsAABC = []
    for i in range(0,24):
        delay_hourly_avg = 0
        hour_count = 0
        for j in range(len(data_cloudAABC.departureTimes)):
            if data_cloudAABC.departureTimes[j] > i * 3600000 and data_cloudAABC.departureTimes[j] < (i+1) * 3600000:
                delay_hourly_avg += data_cloudAABC.timeSystem[j]
                hour_count += 1
        delay_hourly_avg /= hour_count
        delay_hourly_avgsAABC.append(delay_hourly_avg)


    #%% ABCC
    # data storage object
    dataABCC = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    data_cloudABCC = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    
    # simulator
    s_ABCC = sim.Simulator(dataABCC, data_cloudABCC, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s_ABCC.CloudServerServTime = [200, 500, 1000, 1000]
    s_ABCC.CloudServerCosts = [1, 0.4, 0.1, 0.1]
    
    print_everything = False
    dataABCC, data_cloudABCC, time, _, _ = s_ABCC.simulate(print_everything)
    
    print('A-B-C-C simulation')
    print('-'*40)
    print(f'Average Queueing Delay [ms] = {(dataABCC.delay + data_cloudABCC.delay) / (dataABCC.dep + data_cloudABCC.dep)}')
    print(f'Loss Probability = {data_cloudABCC.toCloud/dataABCC.arr}')
    print(f'Average number of users = {(dataABCC.ut + data_cloudABCC.ut)/time}')
    print(f'Total Operational Cost = {sum(s_ABCC.FogBusyTime * s_ABCC.FogNodesCosts) + sum(s_ABCC.CloudServerBusyTime * s_ABCC.CloudServerCosts)}')
    print(f'Micro Data Center Operational Cost = {sum(s_ABCC.FogBusyTime * s_ABCC.FogNodesCosts)}')
    print(f'Cloud Data Center Operational Cost = {sum(s_ABCC.CloudServerBusyTime * s_ABCC.CloudServerCosts)}')
    
    # Average queueing delay with progressively faster MDC service
    costs_hourlyABCC = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloudABCC.departureTimes)):
            if data_cloudABCC.departureTimes[j] > i * 3600000 and data_cloudABCC.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloudABCC.costs[j]
        costs_hourlyABCC.append(cost_hourly)

    delay_hourly_avgsABCC = []
    for i in range(0,24):
        delay_hourly_avg = 0
        hour_count = 0
        for j in range(len(data_cloudABCC.departureTimes)):
            if data_cloudABCC.departureTimes[j] > i * 3600000 and data_cloudABCC.departureTimes[j] < (i+1) * 3600000:
                delay_hourly_avg += data_cloudABCC.timeSystem[j]
                hour_count += 1
        delay_hourly_avg /= hour_count
        delay_hourly_avgsABCC.append(delay_hourly_avg)


    #%% BCAA
    # data storage object
    dataBCAA = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    data_cloudBCAA = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    
    # simulator
    s = sim.Simulator(dataBCAA, data_cloudBCAA, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s.CloudServerServTime = [500, 1000, 200, 200]
    s.CloudServerCosts = [0.4, 0.1, 1, 1]
    
    print_everything = False
    dataBCAA, data_cloudBCAA, time, _, _ = s.simulate(print_everything)
    
    print('B-C-A-A simulation')
    print('-'*40)
    print(f'Average Queueing Delay [ms] = {(dataBCAA.delay + data_cloudBCAA.delay) / (dataBCAA.dep + data_cloudBCAA.dep)}')
    print(f'Loss Probability = {data_cloudBCAA.toCloud/dataBCAA.arr}')
    print(f'Average number of users = {(dataBCAA.ut + data_cloudBCAA.ut)/time}')
    print(f'Total Operational Cost = {sum(s.FogBusyTime * s.FogNodesCosts) + sum(s.CloudServerBusyTime * s.CloudServerCosts)}')
    print(f'Micro Data Center Operational Cost = {sum(s.FogBusyTime * s.FogNodesCosts)}')
    print(f'Cloud Data Center Operational Cost = {sum(s.CloudServerBusyTime * s.CloudServerCosts)}')

    costs_hourlyBCAA = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloudBCAA.departureTimes)):
            if data_cloudBCAA.departureTimes[j] > i * 3600000 and data_cloudBCAA.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloudBCAA.costs[j]
        costs_hourlyBCAA.append(cost_hourly)
        
    delay_hourly_avgsBCAA = []
    for i in range(0,24):
        delay_hourly_avg = 0
        hour_count = 0
        for j in range(len(data_cloudBCAA.departureTimes)):
            if data_cloudBCAA.departureTimes[j] > i * 3600000 and data_cloudBCAA.departureTimes[j] < (i+1) * 3600000:
                delay_hourly_avg += data_cloudBCAA.timeSystem[j]
                hour_count += 1
        delay_hourly_avg /= hour_count
        delay_hourly_avgsBCAA.append(delay_hourly_avg)
    
    
    #%% CBAA
    # data storage object
    dataCBAA = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    data_cloudCBAA = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    
    # simulator
    s = sim.Simulator(dataCBAA, data_cloudCBAA, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s.CloudServerServTime = [1000, 500, 200, 200]
    s.CloudServerCosts = [0.1, 0.4, 1, 1]
    
    print_everything = False
    dataCBAA, data_cloudCBAA, time, _, _ = s.simulate(print_everything)
    
    print('C-B-A-A simulation')
    print('-'*40)
    print(f'Average Queueing Delay [ms] = {(dataCBAA.delay + data_cloudCBAA.delay) / (dataCBAA.dep + data_cloudCBAA.dep)}')
    print(f'Loss Probability = {data_cloudCBAA.toCloud/dataCBAA.arr}')
    print(f'Average number of users = {(dataCBAA.ut + data_cloudCBAA.ut)/time}')
    print(f'Total Operational Cost = {sum(s.FogBusyTime * s.FogNodesCosts) + sum(s.CloudServerBusyTime * s.CloudServerCosts)}')
    print(f'Micro Data Center Operational Cost = {sum(s.FogBusyTime * s.FogNodesCosts)}')
    print(f'Cloud Data Center Operational Cost = {sum(s.CloudServerBusyTime * s.CloudServerCosts)}')

    costs_hourlyCBAA = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloudCBAA.departureTimes)):
            if data_cloudCBAA.departureTimes[j] > i * 3600000 and data_cloudCBAA.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloudCBAA.costs[j]
        costs_hourlyCBAA.append(cost_hourly)
        
    delay_hourly_avgsCBAA = []
    for i in range(0,24):
        delay_hourly_avg = 0
        hour_count = 0
        for j in range(len(data_cloudCBAA.departureTimes)):
            if data_cloudCBAA.departureTimes[j] > i * 3600000 and data_cloudCBAA.departureTimes[j] < (i+1) * 3600000:
                delay_hourly_avg += data_cloudCBAA.timeSystem[j]
                hour_count += 1
        delay_hourly_avg /= hour_count
        delay_hourly_avgsCBAA.append(delay_hourly_avg)
    
    
    #%% Plot compared hourly cost and delay of the best 3 configurations

    fig, ax = plt.subplots(figsize=(14, 4))
    x = np.array([*range(0,24)])
    ax = plt.subplot()
    w = 0.3
    plt.grid(axis='y',zorder=0)
    ax.bar(x, costs_hourlyAABC, width=w, align='center', zorder=3, label='A-A-B-C')
    ax.bar(x-w, costs_hourlyBCAA, width=w, align='center', zorder=3, label='B-C-A-A')
    ax.bar(x+w, costs_hourlyCBAA, width=w, align='center', zorder=3, label='C-B-A-A')
    ax.autoscale(tight=True)
    plt.legend()
    plt.xticks(np.arange(0, 24, 1))
    plt.xlabel("time [hours]")
    plt.ylabel("Cost")
    plt.title('Overall hourly cost of the cloud system')
    plt.show()
    
    fig, ax = plt.subplots(figsize=(14, 4))
    x = np.array([*range(0,24)])
    ax = plt.subplot()
    w = 0.3
    plt.grid(axis='y',zorder=0)
    ax.bar(x, delay_hourly_avgsAABC, width=w, align='center', zorder=3, label='A-A-B-C')
    ax.bar(x-w, delay_hourly_avgsBCAA, width=w, align='center', zorder=3, label='B-C-A-A')
    ax.bar(x+w, delay_hourly_avgsCBAA, width=w, align='center', zorder=3, label='C-B-A-A')
    ax.autoscale(tight=True)
    plt.legend()
    plt.xticks(np.arange(0, 24, 1))
    plt.xlabel("time [hours]")
    plt.ylabel("Queueing delay [ms]")
    plt.title('Average hourly queueing delay in the overall system')
    plt.show()
    

