'''
Exercise 1
'''

import random
import numpy as np
from matplotlib import pyplot as plt
import simulator_class2 as sim

random.seed(42)
np.random.seed(42)

if __name__ == '__main__':
        
    # PARAMS
    SERVICE=100
    LOAD = 2
    ARRIVAL = SERVICE/LOAD

    # SYSTEM PARAMS 
    BUFFER_SIZE = 25 #float('inf')
    FOG_NODES = 1 # number of fog nodes
    f=0.7
    SERVICE_CLOUD=50
    CLOUD_BUFFER_SIZE = 100
    CLOUD_SERVERS= 1
    
    # SIMULATION PARAMS
    SIM_TIME = 500000
    X=[]
    X_transient = []
    num_sim=50
    xj=[]
    for seed in range(num_sim):
        random.seed(seed)
        np.random.seed(seed)

        # data storage object
        data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
        data_cloud = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)

        # simulator
        s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, SERVICE_CLOUD)
        print_everything = False
        data, data_cloud, time, _, _ = s.simulate(print_everything)

        n = len(data_cloud.waitingDelay)
        x = np.mean(data_cloud.waitingDelay)

        xj.append(data_cloud.waitingDelay)

        x = np.mean(data_cloud.waitingDelay)
        x_tr = np.mean(data_cloud.waitingDelay[250:])
        X.append(x)
        X_transient.append(x_tr)
        # cumulate statistics
        #print(data_cloud.waitingDelay)
    X_mean=np.mean(X)
    S=np.std(X)
    X_mean_tr=np.mean(X_transient)
    S_tr=np.std(X_transient)
    print(f'Average delay = {X_mean} +- {3.090 * S / np.sqrt(num_sim)} (confidence 99.8%)')
    print(f'Average delay (without transient)= {X_mean_tr} +- {3.090 * S_tr / np.sqrt(num_sim)} (confidence 99.8%)')
    
    random.seed(42)
    np.random.seed(42)
    
    # data storage object
    data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
    data_cloud = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)

    # simulator
    s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, SERVICE_CLOUD)
    print_everything = False
    data, data_cloud, time, _, _ = s.simulate(print_everything)

    XJ = np.zeros(n)
    for xx in xj:
        XJ += np.array(xx)
    XJ /= num_sim

    xk_list = []
    Rk = []
    for k in range(n):
        xk = np.mean(XJ[k:])
        xk_list.append(xk)
        Rk.append((xk - x) / x)

    rolling_mean = []
    rolling_var = []

    for i in range(1,n):
        mean = np.mean(data_cloud.waitingDelay[:i])
        var = np.std(data_cloud.waitingDelay[:i])
        rolling_mean.append(mean)
        rolling_var.append(var)

        
    
    plt.fill_between(np.linspace(0,n,n-1),(np.array(rolling_mean[:n])+np.array(rolling_var[:n])),(np.array(rolling_mean[:n])-np.array(rolling_var[:n])),alpha=0.5, color='lightcoral')
    plt.plot(data_cloud.waitingDelay[0:n], label='Waiting delay')
    
    plt.plot(rolling_mean[:n], '--', label='running mean', c='red')
    #plt.plot(Rk[0:500], label='Rk')
    plt.legend()
    plt.grid()
    plt.xlabel("Packets")
    plt.ylabel("Waiting Delay [ms]")
    plt.show()

    plt.plot(xk_list, label='xk')
    plt.plot(np.ones(n)*x, label='mean')
    plt.grid()
    plt.legend()
    plt.xlabel("Packets")
    plt.ylabel("xk")
    #plt.ylim([0,3000])
    plt.show()

    plt.plot(Rk, label='Rk')
    plt.grid()
    plt.legend()
    plt.xlabel("Packets")
    plt.ylabel("Rk")
    plt.show()   



