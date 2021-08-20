'''
Exercise 3b
'''

import random
import numpy as np
from matplotlib import pyplot as plt
import simulator_class2 as sim

random.seed(42)
np.random.seed(42)

if __name__ == '__main__':
    
    Tq = 1500 # max average queueing time
    FOG_NODES_NUM = [*range(1, 11, 1)]
    
    num_sim = 1
    tot_queueing_delay = np.zeros(len(FOG_NODES_NUM))
    for seed in range(num_sim):
        random.seed(seed)
        np.random.seed(seed)
        queueing_delay = []
        for FOG_NODES in FOG_NODES_NUM:
        
            # MDC
            ARRIVAL = 500
            SERVICE = 1000
            LOAD = SERVICE/ARRIVAL
            BUFFER_SIZE = 10
            #FOG_NODES = 1
            
            # CDC
            f = 0.8
            SERVICE_CLOUD = 100
            CLOUD_BUFFER_SIZE = 20
            CLOUD_SERVERS = 1
            
            # SIMULATION PARAMS
            SIM_TIME = 300000
            
            # data storage object
            data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[])
            data_cloud = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[])
        
            # simulator
            s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                              FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                              SERVICE_CLOUD)
            print_everything = False
            data, data_cloud, time, _, _ = s.simulate(print_everything)
            
            # cumulate statistics
            queueing_delay.append((data.delay + data_cloud.delay) / (data.dep + data_cloud.dep))
        tot_queueing_delay += np.array(queueing_delay)
    # average multiple simulations 
    tot_queueing_delay /= num_sim
    
    # Average queueing delay with progressively faster MDC service
    plt.plot(FOG_NODES_NUM, tot_queueing_delay, label='Queueing delay')
    plt.plot(Tq * np.ones(11) , '--', label='Tq')
    plt.grid()
    plt.legend()
    plt.xlabel("MDC fog nodes")
    plt.ylabel("Average queueing delay [ms]")
    plt.title('Average queueing delay with progressively more MDC fog nodes')
    plt.show()

