'''
Exercise 4
'''

import numpy as np
from matplotlib import pyplot as plt
import simulator_class as sim

np.random.seed(42)

if __name__ == '__main__':
    
    tot_busy = []
    tot_op = []
    LOADS = np.linspace(1e-5,13,100).tolist()
    ASSIGMENT_METHODS = ['Sorted','RandomAssign','RoundRobin','LeastCostly']
    
    for ASSIGMENT_METHOD in ASSIGMENT_METHODS:
        
        load_list=[]
        busy_times = []
        op_cost = []
        
        for LOAD in LOADS:
            
            # DATA OBJECT
            data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
            
            # SIMULATION PARAMETERS
            #ARRIVAL = 12.0
            SERVICE = 1000.0
            ARRIVAL = SERVICE/LOAD
            #LOAD = SERVICE/ARRIVAL
            BUFFER_SIZE = 5
            FOG_NODES = 1
            SIM_TIME = 300000
    
            # simulator
            s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                              BUFFER_SIZE, FOG_NODES, SIM_TIME)
            print_everything = False
            data, time, busy_time, operational_costs = s.simulate(print_everything, 
                                                                  ASSIGMENT_METHOD)
            
            # cumulate statistics
            load_list.append(LOAD)
            busy_times.append(busy_time)
            op_cost.append(operational_costs)
            
        tot_busy.append(busy_times)
        tot_op.append(op_cost)
    
    colors = [['orangered','deepskyblue','lime','orange'],
              ['maroon','navy','darkgreen','chocolate']]
    # Loss probability vs Load
    for i in range(len(tot_busy)):
        plt.plot(load_list, tot_busy[i], '-', linewidth=0.7, c=colors[1][i], label=f'Method={ASSIGMENT_METHODS[i]}')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Busy time")
    #plt.xlim([0,20])
    #plt.ylim([0,1])
    plt.title('Busy time vs Load')
    plt.show()
    
    # Avg time spent in system vs Load
    for i in range(len(tot_op)):
        plt.plot(load_list, tot_op[i], '.-', linewidth=0.5, c=colors[1][i], label=f'Method={ASSIGMENT_METHODS[i]}')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Operational costs")
    #plt.xlim([0,20])
    plt.title('Operational costs vs Load')
    plt.show()



