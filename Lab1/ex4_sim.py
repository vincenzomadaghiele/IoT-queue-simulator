'''
Exercise 4
'''

import numpy as np
import simulator_class as sim

np.random.seed(42)

if __name__ == '__main__':
    
    ASSIGMENT_METHODS = ['Sorted','RandomAssign','RoundRobin','LeastCostly']
    
    print('CONSTANT AVERAGE SERVICE RATE')
    print('-'*40)
    for ASSIGMENT_METHOD in ASSIGMENT_METHODS:
                            
        # DATA OBJECT
        data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
        
        # SIMULATION PARAMETERS
        #ARRIVAL = 12.0
        LOAD = 5
        SERVICE = 1000.0
        ARRIVAL = SERVICE/LOAD
        #LOAD = SERVICE/ARRIVAL
        BUFFER_SIZE = 5
        FOG_NODES = 5
        SIM_TIME = 300000

        # simulator
        s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                          BUFFER_SIZE, FOG_NODES, SIM_TIME)
        # insert constant service rate for all fog Nodes
        s.FogNodesServTime = [SERVICE for fogNode in range(FOG_NODES)]
        s.FogNodesCosts = [0.2, 0.4, 0.6, 0.8, 1]
        print_everything = False
        data, time, busy_time, operational_cost = s.simulate(print_everything, 
                                                              ASSIGMENT_METHOD)
        
        print(f'Assignment method: {ASSIGMENT_METHOD}')
        print(f'Costs: {s.FogNodesCosts}')
        print(f'Busy times: {busy_time/time}')
        print(f'Operational cost: {operational_cost}')
        print(f'Average queueing delay: {data.delay/data.dep}')
        print()
    print()
    print('DIFFERENT AVERAGE SERVICE RATE')
    print('-'*40)
    for ASSIGMENT_METHOD in ASSIGMENT_METHODS:
                            
        # DATA OBJECT
        data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
        
        # SIMULATION PARAMETERS
        #ARRIVAL = 12.0
        LOAD = 5
        SERVICE = 1000.0
        ARRIVAL = SERVICE/LOAD
        #LOAD = SERVICE/ARRIVAL
        BUFFER_SIZE = 5
        FOG_NODES = 5
        SIM_TIME = 300000

        # simulator
        s = sim.Simulator(data, LOAD, SERVICE, ARRIVAL, 
                          BUFFER_SIZE, FOG_NODES, SIM_TIME)
        print_everything = False
        data, time, busy_time, operational_cost = s.simulate(print_everything, 
                                                              ASSIGMENT_METHOD)
        
        print(f'Assignment method: {ASSIGMENT_METHOD}')
        print(f'Costs: {s.FogNodesCosts}')
        print(f'Busy times: {busy_time/time}')
        print(f'Operational cost: {operational_cost}')
        print(f'Average queueing delay: {data.delay/data.dep}')
        print()
