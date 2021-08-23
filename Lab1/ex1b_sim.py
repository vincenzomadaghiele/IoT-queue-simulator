'''
Exercise 1b
'''

import random
import numpy as np
from matplotlib import pyplot as plt
import simulator_class as sim

random.seed(42)
np.random.seed(42)

if __name__ == '__main__':
    
    tot_loss_pr = [] 
    tot_time_sys = []
    tot_th_av_time_sys_list = []
    tot_pB_list = []
    LOADS = np.linspace(1e-5,13,100).tolist()
    BUFFER_SIZES = [3,5,10]
    
    for BUFFER_SIZE in BUFFER_SIZES:
        
        load_list=[]
        loss_pr = []
        time_sys = []
        pB_list = []
        th_av_time_sys_list = []
        
        for LOAD in LOADS:
            
            # DATA OBJECT
            data = sim.Measure()
            
            # SIMULATION PARAMETERS
            SERVICE = 1000.0
            ARRIVAL = SERVICE/LOAD
            FOG_NODES = 1
            SIM_TIME = 300000
    
            # simulator
            s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                              BUFFER_SIZE, FOG_NODES, SIM_TIME)
            print_everything = False
            data, time, _, _ = s.simulate(print_everything)
            
            # cumulate statistics
            load_list.append(LOAD)
            loss_pr.append(data.toCloud/data.arr)
            time_sys.append(data.delay/data.dep)
            
            # theoretical value for average time in the system
            th_av_num_us = 0
            for i in range(1,BUFFER_SIZE+FOG_NODES+1):
                pi = ((1 - LOAD) / (1 - LOAD**(BUFFER_SIZE+FOG_NODES+1))) * (LOAD**i)
                th_av_num_us += i * pi
            pB = ((1 - LOAD) / (1 - LOAD**(BUFFER_SIZE+FOG_NODES+1))) * (LOAD**(BUFFER_SIZE+FOG_NODES))
            exp_lambd = (1/ARRIVAL) - ((1/ARRIVAL)*pB)
            th_av_time_sys = th_av_num_us / exp_lambd
            pB_list.append(pB)
            th_av_time_sys_list.append(th_av_time_sys)
            
        tot_loss_pr.append(loss_pr)
        tot_time_sys.append(time_sys)
        tot_th_av_time_sys_list.append(th_av_time_sys_list)
        tot_pB_list.append(pB_list)
    
    
    #%% Loss probability vs Load

    colors = [['navy','darkorange','darkgreen'],
              ['tab:blue','tab:orange','tab:green']]
    for i in range(len(tot_loss_pr)):
        plt.plot(load_list, tot_loss_pr[i], '-', linewidth=0.7, c=colors[1][i], label=f'Simluated Buf={BUFFER_SIZES[i]}')
        #plt.plot(load_list, tot_pB_list[i], linewidth=0.5, c=colors[0][i], label=f'Theoretical B={BUFFER_SIZES[i]}')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Forwarding probability")
    #plt.xlim([0,20])
    plt.ylim([0,1])
    plt.title('Forwarding probability vs Load')
    plt.show()
    
    # Loss probability vs Load (zoomed)
    for i in range(len(tot_loss_pr)):
        plt.plot(load_list, tot_loss_pr[i], '.-', linewidth=0.5, c=colors[1][i], label=f'Simluated Buf={BUFFER_SIZES[i]}')
        plt.plot(load_list, tot_pB_list[i], linewidth=0.5, c=colors[0][i], label=f'Theoretical Buf={BUFFER_SIZES[i]}')
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Forwarding probability")
    plt.xlim([0,3])
    plt.ylim([0,1])
    plt.title('Forwarding probability vs Load (zoomed)')
    plt.show()

    
    # Avg time spent in system vs Load
    for i in range(len(tot_time_sys)):
        plt.plot(load_list, tot_time_sys[i], '.-', linewidth=0.5, c=colors[1][i], label=f'Simulated Buf={BUFFER_SIZES[i]}')
        plt.plot(load_list, tot_th_av_time_sys_list[i], linewidth=1, c=colors[0][i], label=f'Theoretical Buf={BUFFER_SIZES[i]}')
    plt.grid()
    plt.legend(loc='lower right', ncol = 2)
    plt.xlabel("Load")
    plt.ylabel("Avgerage time [ms]")
    #plt.xlim([0,14])
    plt.ylim([-1000,13000])
    plt.title('Avg time spent in system vs Load')
    plt.show()

