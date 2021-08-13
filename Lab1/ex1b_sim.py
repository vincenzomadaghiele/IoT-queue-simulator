'''
Exercise 1b
'''

import numpy as np
from matplotlib import pyplot as plt
import simulator_class as sim

np.random.seed(42)

if __name__ == '__main__':
    
    tot_loss_pr = [] 
    tot_time_sys = []
    LOADS = np.linspace(1e-5,10,50)
    BUFFER_SIZES = [1,3,5]
    
    for BUFFER_SIZE in BUFFER_SIZES:
        
        loss_pr = []
        time_sys = []
        
        for LOAD in LOADS:
            
            # DATA OBJECT
            data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
            
            # SIMULATION PARAMETERS
            #LOAD = 0.85
            SERVICE = 10.0
            ARRIVAL = SERVICE/LOAD
            #BUFFER_SIZE = 0 #float('inf')
            FOG_NODES = 1
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
    for p in tot_loss_pr:
        plt.scatter(LOADS,p, s=7, label='B=..')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Loss probability")
    plt.xlim([0,10])
    plt.ylim([0,1])
    plt.show()


