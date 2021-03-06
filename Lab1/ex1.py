'''
Exercise 1
'''

import random
import numpy as np
from matplotlib import pyplot as plt
import simulator_class as sim

random.seed(42)
np.random.seed(42)

if __name__ == '__main__':
    
    load_list=[]
    loss_pr=[]
    avg_users=[]

    for SERVICE in range (1,380,2):
        
        # data storage object
        data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[])
        
        ARRIVAL = 30.0
        LOAD = SERVICE/ARRIVAL
        
        # SYSTEM PARAMS 
        BUFFER_SIZE = 0 
        FOG_NODES = 1 
        
        # SIMULATION PARAMS
        SIM_TIME = 300000

        # simulator
        s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, FOG_NODES, SIM_TIME)
        print_everything = False
        data, time, _, _ = s.simulate(print_everything)
        
        # cumulate statistics
        load_list.append(LOAD)
        loss_pr.append(data.toCloud/data.arr)
        avg_users.append(data.ut/time)
    
    # Loss probability vs Load
    plt.plot(np.array(load_list),((np.array(load_list)))/(1+np.array(load_list)),label='Theoretical values')
    #plt.scatter(load_list,loss_pr, s=7, c='r', label='Simulated values')
    plt.plot(load_list,loss_pr, label='Simulated values')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Forwarding probability")
    plt.title("Probability to forward a packet to the CDC")
    plt.ylim([0,1])
    plt.show()

    # Avg number of users vs Load    
    plt.plot(np.array(load_list),np.array(load_list)/(1+np.array(load_list)),label='Theoretical values')
    #plt.scatter(load_list,avg_users, s=7, c='r', label='Simulated values')
    plt.plot(load_list,avg_users, label='Simulated values')

    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Avg number of users")
    plt.title("Average number of users in the system")
    plt.ylim([0,1])
    plt.show()


