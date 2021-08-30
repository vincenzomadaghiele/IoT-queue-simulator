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

    # simulate AA
    
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
    CLOUD_SERVERS = 2
    
    # SIMULATION PARAMS
    SIM_TIME = 86400000 # 24 hours simulation
    
    # data storage object
    data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                       [],[],[],[],[],[],[],[],[])
    data_cloud = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                           [],[],[],[],[],[],[],[],[])
    
    # simulator
    s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                      FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                      SERVICE_CLOUD,f_av_arrival, f_f)
    
    # insert constant service rate for all fog Nodes
    s.CloudServerServTime = [200, 200]
    s.CloudServerCosts = [1, 1]
    
    print_everything = False
    data, data_cloud, time, _, _ = s.simulate(print_everything)
    
    print('A-A simulation')
    print('-'*40)
    print(f'Average Queueing Delay [ms] = {(data.delay + data_cloud.delay) / (data.dep + data_cloud.dep)}')
    print(f'Loss Probability = {data_cloud.toCloud/data.arr}')
    print(f'Average number of users = {(data.ut + data_cloud.ut)/time}')
    print(f'Total Operational Cost = {sum(s.FogBusyTime * s.FogNodesCosts) + sum(s.CloudServerBusyTime * s.CloudServerCosts)}')
    
    
    # Average queueing delay with progressively faster MDC service
    costs_hourlyAA = []
    for i in range(0,24):
        cost_hourly = 0
        for j in range(len(data_cloud.departureTimes)):
            if data_cloud.departureTimes[j] > i * 3600000 and data_cloud.departureTimes[j] < (i+1) * 3600000:
                cost_hourly += data_cloud.costs[j]
        costs_hourlyAA.append(cost_hourly)

    delay_hourly_avgsAA = []
    for i in range(0,24):
        delay_hourly_avg = 0
        hour_count = 0
        for j in range(len(data_cloud.departureTimes)):
            if data_cloud.departureTimes[j] > i * 3600000 and data_cloud.departureTimes[j] < (i+1) * 3600000:
                delay_hourly_avg += data_cloud.timeSystem[j]
                hour_count += 1
        delay_hourly_avg /= hour_count
        delay_hourly_avgsAA.append(delay_hourly_avg)
    
    plt.grid(axis='y',zorder=0)
    plt.bar([*range(0,24)],costs_hourlyAA, zorder=3)
    plt.xticks(np.arange(0, 25, 2))
    plt.xlabel("time [hours]")
    plt.ylabel("Cost")
    plt.title('Hourly cost of the cloud server')
    plt.show()
    
    plt.grid(axis='y',zorder=0)
    plt.bar([*range(0,24)],delay_hourly_avgsAA, zorder=3)
    plt.xticks(np.arange(0, 25, 2))
    plt.xlabel("time [hours]")
    plt.ylabel("Delay [ms]")
    plt.title('Hourly delay of the cloud server')
    plt.show()
    
    
    #%% Hourly lost packets by type
    
    # Count how many pkts for each hour
    hourly_arrivals_tot = []
    for i in range(0,24):
        hourly_arrivals = 0
        for j in range(len(data.arrivalTimes)):
            if data.arrivalTimes[j] > i * 3600000 and data.arrivalTimes[j] < (i+1) * 3600000:
                hourly_arrivals += 1
        hourly_arrivals_tot.append(hourly_arrivals)

    # Count lost pkts for each hour by type
    pkts_lost_hourlyA = []
    pkts_lost_hourlyB = []
    for i in range(0,24):
        lost_hourlyA = 0
        lost_hourlyB = 0
        for j in range(len(data_cloud.lossTimes)):
            if data_cloud.lossTimes[j] > i * 3600000 and data_cloud.lossTimes[j] < (i+1) * 3600000:
                if data_cloud.lostPktTypes[j] == 'A':
                    lost_hourlyA += 1
                elif data_cloud.lostPktTypes[j] == 'B':
                    lost_hourlyB += 1
        pkts_lost_hourlyA.append(lost_hourlyA)
        pkts_lost_hourlyB.append(lost_hourlyB)
        
    # percentage of lost packets by type each hour
    hourly_perc_lostA = np.array(pkts_lost_hourlyA) / np.array(hourly_arrivals_tot)
    hourly_perc_lostB = np.array(pkts_lost_hourlyB) / np.array(hourly_arrivals_tot)
    

    #%% Hourly delays by packets type

    hourly_delayA_tot = []
    for i in range(0,24):
        hourly_delayA = 0
        count_hourly = 0
        for j in range(len(data_cloud.typeAarrival)):
            if data_cloud.typeAarrival[j] > i * 3600000 and data_cloud.typeAarrival[j] < (i+1) * 3600000:
                hourly_delayA += data_cloud.typeAdelay[j]
                count_hourly += 1
        hourly_delayA /= count_hourly
        hourly_delayA_tot.append(hourly_delayA)

    hourly_delayB_tot = []
    for i in range(0,24):
        hourly_delayB = 0
        count_hourly = 0
        for j in range(len(data_cloud.typeBarrival)):
            if data_cloud.typeBarrival[j] > i * 3600000 and data_cloud.typeBarrival[j] < (i+1) * 3600000:
                hourly_delayB += data_cloud.typeBdelay[j]
                count_hourly += 1
        hourly_delayB /= count_hourly
        hourly_delayB_tot.append(hourly_delayB)
    
    
    #%% Plot comparison by packet Type
    
    plt.grid(axis='y',zorder=0)
    plt.bar([*range(0,24)],hourly_perc_lostB, zorder=3,label='Type B')
    plt.bar([*range(0,24)],hourly_perc_lostA, zorder=3,label='Type A')
    #plt.bar([*range(0,24)],lossPr_hourly_1000, zorder=3, alpha=.5)
    plt.xticks(np.arange(0, 25, 2))
    plt.ylim([0,1])
    plt.legend()
    plt.xlabel("time [hours]")
    plt.ylabel("Loss probability")
    plt.title('Hourly loss probability')
    plt.show()
    
    fig, ax = plt.subplots(figsize=(14, 4))
    x = np.array([*range(0,24)])
    ax = plt.subplot()
    w = 0.3
    plt.grid(axis='y',zorder=0)
    #ax.bar(x, hourly_delayA_tot, width=w, align='center', zorder=3, label='A-A-B-C')
    ax.bar(x-w/2, hourly_delayB_tot, width=w, align='center', zorder=3, label='Type B')
    ax.bar(x+w/2, hourly_delayA_tot, width=w, align='center', zorder=3, label='Type A')
    ax.autoscale(tight=True)
    plt.legend()
    plt.xticks(np.arange(0, 24, 1))
    plt.xlabel("time [hours]")
    plt.ylabel("Queueing delay [ms]")
    plt.title('Average hourly queueing delay in the overall system')
    plt.show()


