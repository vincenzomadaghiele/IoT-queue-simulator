'''
Exercise 4a
'''

import random
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import simulator_class2 as sim

random.seed(42)
np.random.seed(42)

if __name__ == '__main__':
    
    # define interest points
    f_x_points = np.array([0,5,10,12,18,20,24.5]) * 3600000
    f_y_points = [0.8,0.6,0.2,0.4,0.25,0.45,0.8]
    # interpolate points
    f_av_arrival = interp1d(f_x_points, f_y_points, kind='quadratic')
    x = [*range(0, 86400000, 1000)]
    y = f_av_arrival(x) # f(x) is the inter-arrival variation in a day

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

    # simulate
    num_sim = 1
    for seed in range(num_sim):
        random.seed(seed)
        np.random.seed(seed)
        
        # Micro Data Center (MDC)
        SERVICE = 1000
        ARRIVAL = 300
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
        print_everything = False
        data, data_cloud, time, _, _ = s.simulate(print_everything)
        
        print(f'Average Queueing Delay [ms] = {(data.delay + data_cloud.delay) / (data.dep + data_cloud.dep)}')
        print(f'Loss Probability = {data_cloud.toCloud/data.arr}')
        print(f'Average number of users = {(data.ut + data_cloud.ut)/time}')
    
    
    # Average queueing delay with progressively faster MDC service
    
    delay_hourly_avgs = []
    for i in range(0,24):
        delay_hourly_avg = 0
        hour_count = 0
        for j in range(len(data_cloud.departureTimes)):
            if data_cloud.departureTimes[j] > i * 3600000 and data_cloud.departureTimes[j] < (i+1) * 3600000:
                delay_hourly_avg += data_cloud.timeSystem[j]
                hour_count += 1
        delay_hourly_avg /= hour_count
        delay_hourly_avgs.append(delay_hourly_avg)

    plt.grid(axis='y',zorder=0)
    plt.bar([*range(0,24)],delay_hourly_avgs, zorder=3)
    plt.xticks(np.arange(0, 25, 2))
    plt.xlabel("time [hours]")
    plt.ylabel("Average queueing delay [ms]")
    plt.title('Average hourly queueing delay')
    plt.show()

    arrived_pkts_hourly = []
    for i in range(0,24):
        arrived_pkts = 0
        for j in range(len(data_cloud.arrivalTimes)):
            if data_cloud.arrivalTimes[j] > i * 3600000 and data_cloud.arrivalTimes[j] < (i+1) * 3600000:
                arrived_pkts += 1
        arrived_pkts_hourly.append(arrived_pkts)

    lost_pkts_hourly = []
    for i in range(0,24):
        lost_pkts = 0
        for j in range(len(data_cloud.lossTimes)):
            if data_cloud.lossTimes[j] > i * 3600000 and data_cloud.lossTimes[j] < (i+1) * 3600000:
                lost_pkts += 1
        lost_pkts_hourly.append(lost_pkts)

    lossPr_hourly = (np.array(lost_pkts_hourly) / np.array(arrived_pkts_hourly)).tolist()
    plt.grid(axis='y',zorder=0)
    plt.bar([*range(0,24)],lossPr_hourly, zorder=3)
    plt.xticks(np.arange(0, 25, 2))
    plt.ylim([0,1])
    plt.xlabel("time [hours]")
    plt.ylabel("Loss probability")
    plt.title('Hourly loss probability')
    plt.show()



    
