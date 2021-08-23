'''
Exercise 5
'''
import random
import numpy as np
import simulator_class as sim

np.random.seed(24)
random.seed(24)

if __name__ == '__main__':
    
    DISTRIBUTIONS = ['Exponential','Constant','Uniform']
    NUM_SIMULATIONS = 50
    
    # SIMULATION PARAMETERS
    LOAD = 0.8
    SERVICE = 1000.0
    ARRIVAL = SERVICE/LOAD
    FOG_NODES = 1
    BUFFER_SIZE = float('inf')
    SIM_TIME = 500000
    
    print('DIFFERENT SERVICE TIME DISTRIBUTIONS')
    print('-'*40)
    for DISTRIBUTION in DISTRIBUTIONS:
        mean_time_sys = 0
        mean_avg_usr = 0
        th_av_users=0
        th_av_time_sys=0
        for i in range(NUM_SIMULATIONS):
            # DATA OBJECT
            data = sim.Measure()
            
            # simulator
            s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                              BUFFER_SIZE, FOG_NODES, SIM_TIME)
            print_everything = False
            data, time, _, _ = s.simulate(print_everything, distribution=DISTRIBUTION)
            
            # cumulate statistics
            mean_time_sys += data.delay/data.dep
            mean_avg_usr += data.ut/time
            
        # theoretical value for average time in the system
        if DISTRIBUTION == 'Uniform':
            var = 200
            Cs2 = var / (SERVICE**2)
            th_av_users=LOAD+(LOAD**2)*((1 + Cs2) / (2*(1 - LOAD)))
            th_av_time_sys = SERVICE + (LOAD * SERVICE * ((1 + Cs2) / (2*(1 - LOAD))))
        elif DISTRIBUTION == 'Exponential':
            Cs2 = 1
            th_av_users=LOAD+(LOAD**2)*((1 + Cs2) / (2*(1 - LOAD)))
            th_av_time_sys = 1 / ((1/SERVICE) - (1/ARRIVAL))
        elif DISTRIBUTION == 'Constant':
            Cs2 = 0
            th_av_users=LOAD+(LOAD**2)*((1 + Cs2) / (2*(1 - LOAD)))
            th_av_time_sys = ((2 - LOAD)/ 2) * (1 / ((1/SERVICE) - (1/ARRIVAL)))
            
        # find averages
        mean_time_sys /= NUM_SIMULATIONS
        mean_avg_usr /= NUM_SIMULATIONS
        
        print(f'Distribution: {DISTRIBUTION}')
        print(f'Average time in the system: {mean_time_sys}')        
        print(f'Average number of users: {mean_avg_usr}')   
        print("Theoretical values:\n") 
        print(f'\tAverage time in the system: {th_av_time_sys}')
        print(f'\tAverage number of users: {th_av_users}') 
        print()
