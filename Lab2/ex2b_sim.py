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
    LOAD = 4
    ARRIVAL = SERVICE/LOAD

    # SYSTEM PARAMS 
    BUFFER_SIZE = 7
    FOG_NODES = 1 
    f = 0.7
    SERVICE_CLOUD = 20
    CLOUD_BUFFER_SIZE = 20
    CLOUD_SERVERS = 1
    
    # SIMULATION PARAMS
    SIM_TIME = 800000
    
    time_sys=[]
    lost_pkt=[]
    BUFFERS=np.linspace(0,50,51)
    for CLOUD_BUFFER_SIZE in BUFFERS:
        data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
        data_cloud = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)

        # simulator
        s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                          FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                          SERVICE_CLOUD)
        print_everything = False
        data, data_cloud, time, _, _ = s.simulate(print_everything)

        #time_sys.append(np.mean(data.waitingDelay)+np.mean(data_cloud.waitingDelay))
        time_sys.append((data.delay/data.dep)+(data_cloud.delay/data_cloud.dep))
        lost_pkt.append(data_cloud.toCloud/data.arr)

    plt.plot(BUFFERS, time_sys)
    plt.grid()
    plt.xlabel("CDC buffer size")
    plt.ylabel("Average waiting delay")
    plt.title("Average waiting delay for the whole system")
    plt.show()

    plt.plot(BUFFERS, lost_pkt)
    plt.grid()
    plt.xlabel("CDC buffer size")
    plt.ylabel("Loss probability")
    plt.ylim([0,1])
    plt.title("Probability to lose a packet")
    plt.show()
