'''
Exercise 2a
'''

import random
import numpy as np
from matplotlib import pyplot as plt
import simulator_class2 as sim

random.seed(42)
np.random.seed(42)

if __name__ == '__main__':
        
    # PARAMS
    SERVICE = 100
    LOAD = 1.5
    ARRIVAL = SERVICE/LOAD

    # SYSTEM PARAMS 
    BUFFER_SIZE = 7
    FOG_NODES = 1 
    f = 0.7
    
    SERVICE_CLOUD = 50
    CLOUD_BUFFER_SIZE = 8
    CLOUD_SERVERS = 1
    
    # SIMULATION PARAMS
    SIM_TIME = 1000000
    
    time_tot=[]
    lost_tot=[]
    num_sim=50
    BUFFERS=np.linspace(0,20,21)
    for seed in range(num_sim):
        
        random.seed(seed)
        np.random.seed(seed)
        time_sys=[]
        lost_pkt=[]
        
        for BUFFER_SIZE in BUFFERS:
            
            data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                               [],[],[],[],[],[],[],[],[])
            data_cloud = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],[],
                                     [],[],[],[],[],[],[],[],[])

            # simulator
            s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                              FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                              SERVICE_CLOUD)
            print_everything = False
            data, data_cloud, time, _, _ = s.simulate(print_everything)

            #time_sys.append(np.mean(data.waitingDelay)+np.mean(data_cloud.waitingDelay))
            #time_sys.append((data.delay/data.dep)+(data_cloud.delay/data_cloud.dep))
            time_sys.append((data.delay+data_cloud.delay)/(data.dep+data_cloud.dep))
            lost_pkt.append(data_cloud.toCloud/data.arr)
        time_tot.append(time_sys)
        lost_tot.append(lost_pkt)

    T = np.zeros(len(BUFFERS))
    for t in time_tot:
        T += np.array(t)
    T /= num_sim

    L = np.zeros(len(BUFFERS))
    for l in lost_tot:
        L += np.array(l)
    L /= num_sim

    plt.plot(BUFFERS, T)
    plt.grid()
    plt.xlabel("MDC buffer size")
    plt.ylabel("Average queuing delay [ms]")
    plt.title("Average queuing delay for the whole system")
    plt.show()

    plt.plot(BUFFERS, L)
    plt.grid()
    plt.xlabel("MDC buffer size")
    plt.ylabel("Loss probability")
    #plt.ylim([0,1])
    plt.title("Probability to lose a packet")
    plt.show()
