'''
Exercise 4
'''

import numpy as np
import simulator_class as sim

np.random.seed(42)

if __name__ == '__main__':
    
    ASSIGMENT_METHODS = ['Sorted','RandomAssign','RoundRobin','LeastCostly']
    NUM_SIMULATIONS = 10
    
    # SIMULATION PARAMETERS
    #ARRIVAL = 12.0
    LOAD = 2
    SERVICE = 1000.0
    ARRIVAL = SERVICE/LOAD
    #LOAD = SERVICE/ARRIVAL
    BUFFER_SIZE = 5
    FOG_NODES = 5
    SIM_TIME = 300000
    
    print('CONSTANT AVERAGE SERVICE RATE')
    print('-'*40)
    for ASSIGMENT_METHOD in ASSIGMENT_METHODS:
        mean_busy = np.zeros(FOG_NODES)
        mean_cost = 0
        mean_av_delay = 0
        for i in range(NUM_SIMULATIONS):
            
            # DATA OBJECT
            data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
    
            # simulator
            s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                              BUFFER_SIZE, FOG_NODES, SIM_TIME)
            
            # insert constant service rate for all fog Nodes
            s.FogNodesServTime = [SERVICE for fogNode in range(FOG_NODES)]
            s.FogNodesCosts = [1, 0.8, 0.6, 0.4, 0.2]
            
            # simulate
            print_everything = False
            data, time, busy_time, operational_cost = s.simulate(print_everything, 
                                                                  ASSIGMENT_METHOD)
            
            # cumulate statistics
            mean_busy += np.array(busy_time/time)
            mean_cost += operational_cost
            mean_av_delay += data.delay/data.dep
        
        # compute averages
        mean_busy /= NUM_SIMULATIONS
        mean_cost /= NUM_SIMULATIONS
        mean_av_delay /= NUM_SIMULATIONS
        
        print(f'Assignment method: {ASSIGMENT_METHOD}')
        print(f'Costs: {s.FogNodesCosts}')
        print(f'Busy times: {mean_busy}')
        print(f'Operational cost: {mean_cost}')
        print(f'Average queueing delay: {mean_av_delay}')
        print()
    print()
    print('DIFFERENT AVERAGE SERVICE RATE')
    print('-'*40)
    for ASSIGMENT_METHOD in ASSIGMENT_METHODS:
        mean_busy = np.zeros(FOG_NODES)
        mean_cost = 0
        mean_av_delay = 0
        for i in range(NUM_SIMULATIONS):
            
            # DATA OBJECT
            data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
                
            # simulator
            s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                              BUFFER_SIZE, FOG_NODES, SIM_TIME)
            print_everything = False
            data, time, busy_time, operational_cost = s.simulate(print_everything, 
                                                                  ASSIGMENT_METHOD)
            
            # cumulate statistics
            mean_busy += np.array(busy_time/time)
            mean_cost += operational_cost
            mean_av_delay += data.delay/data.dep
        
        # compute averages
        mean_busy /= NUM_SIMULATIONS
        mean_cost /= NUM_SIMULATIONS
        mean_av_delay /= NUM_SIMULATIONS
        
        print(f'Assignment method: {ASSIGMENT_METHOD}')
        print(f'Costs: {s.FogNodesCosts}')
        print(f'Busy times: {mean_busy}')
        print(f'Operational cost: {mean_cost}')
        print(f'Average queueing delay: {mean_av_delay}')
        print()
