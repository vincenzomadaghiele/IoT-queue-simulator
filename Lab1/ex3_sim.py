'''
Exercise 3
'''

import numpy as np
from matplotlib import pyplot as plt
import simulator_class as sim

np.random.seed(42)

if __name__ == '__main__':
    
    tot_loss_pr = [] 
    tot_time_sys = []
    FOG_NODES_LIST = [1,2]
    BUFFER_SIZES = [5, float('inf')]
    
    for BUFFER_SIZE in BUFFER_SIZES:
        
        loss_pr = []
        time_sys = []
        
        for FOG_NODES in FOG_NODES_LIST:
            
            # DATA OBJECT
            data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
            
            # SIMULATION PARAMETERS
            LOAD = 0.85
            SERVICE = 10.0
            ARRIVAL = SERVICE/LOAD
            #BUFFER_SIZE = 0 #float('inf')
            FOG_NODES = 2
            SIM_TIME = 500000
    
            # simulator
            s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                              BUFFER_SIZE, FOG_NODES, SIM_TIME)
            print_everything = False
            data, time = s.simulate(print_everything)
            
            # cumulate statistics
            loss_pr.append(data.toCloud/data.arr)
            time_sys.append(data.delay/data.dep)
            
        tot_loss_pr.append(loss_pr)
        tot_time_sys.append(time_sys)
    
    # Loss probability vs Load
    for i in range(len(tot_loss_pr)):
        plt.plot(LOADS, tot_loss_pr[i], label=f'B={BUFFER_SIZES[i]}')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Loss probability")
    plt.xlim([0,10])
    plt.ylim([0,1])
    plt.show()
    
    # Avg time spent in system vs Load
    for i in range(len(tot_loss_pr)):
        plt.plot(LOADS, tot_loss_pr[i], label=f'B={BUFFER_SIZES[i]}')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Avg time in system")
    plt.xlim([0,10])
    plt.ylim([0,1])
    plt.show()



