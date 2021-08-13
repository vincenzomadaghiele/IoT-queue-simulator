'''
Exercise 1
'''

import numpy as np
from matplotlib import pyplot as plt
import simulator_class as sim

if __name__ == '__main__':
    
    load_list=[]
    loss_pr=[]
    avg_users=[]

    for SERVICE in range (1,240,2):
        
        # data storage object
        data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
        
        ARRIVAL = 12.0
        LOAD = SERVICE/ARRIVAL
        #SERVICE = 10.0
        
        # SYSTEM PARAMS 
        BUFFER_SIZE = 0 #float('inf')
        FOG_NODES = 1 # number of fog nodes
        
        # SIMULATION PARAMS
        SIM_TIME = 500000

        # simulator
        s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, FOG_NODES, SIM_TIME)
        print_everything = False
        data, time = s.simulate(print_everything)
        
        load_list.append(LOAD)
        loss_pr.append(data.toCloud/data.arr)
        avg_users.append(data.ut/time)
    
    plt.plot(np.array(load_list),np.array(load_list)/(1+np.array(load_list)),label='Theoretical values')
    plt.scatter(load_list,loss_pr, s=7, c='r', label='Simulated values')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Loss probability")
    plt.ylim([0,1])
    plt.show()

    plt.plot(np.array(load_list),np.array(load_list)/(1+np.array(load_list)))
    plt.plot(load_list,avg_users)
    plt.grid()
    plt.xlabel("Load")
    plt.ylabel("Avg number of users")
    plt.show()

    

