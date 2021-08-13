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
    tot_th_av_time_sys_list = []
    LOADS = np.linspace(1e-5,20,50).tolist()
    BUFFER_SIZES = [3,5,7]
    #ARRIVALS = np.linspace(0.5,10,20)[::-1]
    
    for BUFFER_SIZE in BUFFER_SIZES:
        
        load_list=[]
        loss_pr = []
        time_sys = []
        th_av_time_sys_list = []
        
        for LOAD in LOADS:
            
            # DATA OBJECT
            data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
            
            # SIMULATION PARAMETERS
            #ARRIVAL = 12.0
            SERVICE = 1000.0
            ARRIVAL = SERVICE/LOAD
            #LOAD = SERVICE/ARRIVAL
            FOG_NODES = 1
            SIM_TIME = 500000
    
            print(f'Simulating with LOAD = {LOAD}')
            # simulator
            s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                              BUFFER_SIZE, FOG_NODES, SIM_TIME)
            print_everything = False
            data, time = s.simulate(print_everything)
            
            # cumulate statistics
            load_list.append(LOAD)
            loss_pr.append(data.toCloud/data.arr)
            time_sys.append(data.delay/data.dep)
            
            # theoretical value for average time in the system
            th_av_num_us = 0
            for i in range(1,BUFFER_SIZE):
                pi = ((1 - LOAD) / (1 - LOAD**(BUFFER_SIZE+1))) * (LOAD**i)
                th_av_num_us += i * pi
            
            pB = ((1 - LOAD) / (1 - LOAD**(BUFFER_SIZE+1))) * (LOAD**BUFFER_SIZE)
            exp_lambd = (1/ARRIVAL) - ((1/ARRIVAL)*pB)
            th_av_time_sys = th_av_num_us / exp_lambd
            th_av_time_sys_list.append(th_av_time_sys)
            
        tot_loss_pr.append(loss_pr)
        tot_time_sys.append(time_sys)
        tot_th_av_time_sys_list.append(th_av_time_sys_list)
    
    
    # Loss probability vs Load
    for i in range(len(tot_loss_pr)):
        plt.plot(load_list, tot_loss_pr[i], label=f'B={BUFFER_SIZES[i]}')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Loss probability")
    plt.xlim([0,20])
    plt.ylim([0,1])
    plt.show()
    
    # Avg time spent in system vs Load
    for i in range(len(tot_time_sys)):
        plt.plot(load_list, tot_time_sys[i], label=f'B={BUFFER_SIZES[i]}')
        plt.plot(load_list, tot_th_av_time_sys_list[i], label=f'B={BUFFER_SIZES[i]}')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Avg time in system")
    plt.xlim([0,20])
    plt.show()



