'''
Exercise 4a
'''

import random
import numpy as np
from matplotlib import pyplot as plt
import simulator_class2 as sim

random.seed(42)
np.random.seed(42)

def InterArrivalDayFunction(time):
    return 

if __name__ == '__main__':
    
    num_sim = 1
    for seed in range(num_sim):
        random.seed(seed)
        np.random.seed(seed)
        
        # Micro Data Center (MDC)
        SERVICE = 1000
        ARRIVAL = 50
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
        data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
        data_cloud = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
    
        # simulator
        s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                          FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                          SERVICE_CLOUD)
        print_everything = False
        data, data_cloud, time, _, _ = s.simulate(print_everything)
        
        print(f'Average Queueing Delay [ms] = {(data.delay + data_cloud.delay) / (data.dep + data_cloud.dep)}')
        print(f'Loss Probability = {data_cloud.toCloud/data.arr}')
        print(f'Average number of users = {(data.ut + data_cloud.ut)/time}')
        
    #%%
    f_x_points = np.array([0,5,10,12,18,20,22,24]) * 3600000
    f_y_points = [0.8,0.6,0.2,0.4,0.25,0.45,0.6,0.8]
    
    plt.plot(f_x_points, f_y_points)
    plt.xlim([0,86400000])
    plt.ylim([0,1])
    plt.grid()
    plt.show()
    
    x = [*range(0, 86400000, 1)]
    #y = 
    
    '''
    # Average queueing delay with progressively faster MDC service
    #plt.plot(SERVICE_TIMES, tot_queueing_delay, label='Queueing delay')
    #plt.plot(Tq * np.ones(1000) , '--', label='Tq')
    plt.grid()
    plt.legend()
    plt.xlabel("Average service MDC time [ms]")
    plt.ylabel("Average queueing delay [ms]")
    plt.title('Average queueing delay with progressively slower MDC service')
    plt.show()
    '''
