'''
Exercise 3
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
    BUFFER_SIZES = [0,5,float('inf')]
    
    # Buf = [5, inf], FOG_NODES = 2
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
            FOG_NODES = 2
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
            
        tot_loss_pr.append(loss_pr)
        tot_time_sys.append(time_sys)
        tot_th_av_time_sys_list.append(th_av_time_sys_list)
        tot_pB_list.append(pB_list)
        
    # Buf = 5, FOG_NODES = 1
    BUFFER_SIZE = 5
    FOG_NODES = 1

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
        
    tot_loss_pr.append(loss_pr)
    tot_time_sys.append(time_sys)
    tot_th_av_time_sys_list.append(th_av_time_sys_list)
    tot_pB_list.append(pB_list)


    #%% Plot statistics
    
    colors = [['navy','darkorange','darkgreen','darkred'],
              ['tab:blue','tab:orange','tab:green','tab:red']]
    labels = ['Buf=0, Fog=2','Buf=5, Fog=2', 
              'Buf=inf, Fog=2', 'Buf=5, Fog=1']
    # Loss probability vs Load
    for i in range(len(tot_loss_pr)):
        plt.plot(load_list, tot_loss_pr[i], '.-', linewidth=.7, c=colors[1][i], label=labels[i])
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Loss probability")
    plt.ylim([-0.05,1])
    plt.title('Loss probability vs Load')
    plt.show()
    
    # Loss probability vs Load (zoomed)
    for i in range(len(tot_loss_pr)):
        plt.plot(load_list, tot_loss_pr[i], '.-', linewidth=0.5, c=colors[1][i], label=labels[i])
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Loss probability")
    plt.xlim([0,3])
    plt.ylim([0,1])
    plt.title('Loss probability vs Load (zoomed)')
    plt.show()

    # Avg time spent in system vs Load
    for i in range(len(tot_time_sys)):
        plt.plot(load_list, tot_time_sys[i], '.-', linewidth=0.5, c=colors[1][i], label=labels[i])
    plt.grid()
    plt.legend()
    plt.xlabel("Load")
    plt.ylabel("Avgerage time [ms]")
    plt.xlim([0,4])
    plt.title('Avg time spent in system vs Load')
    plt.show()



