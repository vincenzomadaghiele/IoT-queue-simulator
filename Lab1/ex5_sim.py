'''
Exercise 5
'''

import numpy as np
import simulator_class as sim

np.random.seed(42)

if __name__ == '__main__':
    
    DISTRIBUTIONS = ['Exponential','Uniform','Constant']
    NUM_SIMULATIONS = 10
    
    # SIMULATION PARAMETERS
    LOAD = 2
    SERVICE = 1000.0
    ARRIVAL = SERVICE/LOAD
    FOG_NODES = 1
    BUFFER_SIZE = float('inf')
    SIM_TIME = 300000
    
    print('DIFFERENT SERVICE TIME DISTRIBUTIONS')
    print('-'*40)
    for DISTRIBUTION in DISTRIBUTIONS:
        mean_time_sys = 0
        mean_avg_usr = 0
        for i in range(NUM_SIMULATIONS):
            # DATA OBJECT
            data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
            
            # simulator
            s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                              BUFFER_SIZE, FOG_NODES, SIM_TIME)
            print_everything = False
            data, time, _, _ = s.simulate(print_everything, distribution=DISTRIBUTION)
            
            # cumulate statistics
            mean_time_sys += data.delay/data.dep
            mean_avg_usr += data.ut/time
            
            '''
            # theoretical value for average time in the system
            if DISTRIBUTION == 'Uniform':
                var = 500
                Cs2 = var / (SERVICE**2)
                th_av_time_sys = SERVICE + (LOAD * SERVICE * ((1 + Cs2) / (2*(1 - LOAD))))
            elif DISTRIBUTION == 'Exponential':
                Cs2 = 1
                th_av_time_sys = 1 / ((1/SERVICE) - (1/ARRIVAL))
            elif DISTRIBUTION == 'Constant':
                Cs2 = 0
                th_av_time_sys = ((2 - LOAD)/ 2) * (1 / ((1/SERVICE) - (1/ARRIVAL)))
            th_av_time_sys_list.append(th_av_time_sys)
            '''
            
        # find averages
        mean_time_sys /= NUM_SIMULATIONS
        mean_avg_usr /= NUM_SIMULATIONS
        
        print(f'Distribution: {DISTRIBUTION}')
        print(f'Average time in the system: {mean_time_sys}')
        print(f'Average nnumber of users: {mean_avg_usr}')    
        print()
