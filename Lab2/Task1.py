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
    SERVICE = 100
    LOAD = 2
    ARRIVAL = SERVICE/LOAD

    # SYSTEM PARAMS 
    BUFFER_SIZE = 25
    FOG_NODES = 1
    f = 0.7
    SERVICE_CLOUD = 50
    CLOUD_BUFFER_SIZE = 100
    CLOUD_SERVERS = 1
    
    # SIMULATION PARAMS
    SIM_TIME = 800000
    
    # multiple sims
    num_sim = 100
    TRANSIENT_THRESHOLD = 200
    X = []
    X_transient = []
    xj = []
    for seed in range(num_sim):
        random.seed(seed)
        np.random.seed(seed)

        # data storage object
        data = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)
        data_cloud = sim.Measure(0,0,0,0,0,0,0,0,0,0,[],[],0)

        # simulator
        s = sim.Simulator(data, data_cloud, LOAD, SERVICE, ARRIVAL, BUFFER_SIZE, 
                          FOG_NODES, SIM_TIME, f, CLOUD_SERVERS, CLOUD_BUFFER_SIZE, 
                          SERVICE_CLOUD)
        print_everything = False
        data, data_cloud, time, _, _ = s.simulate(print_everything)

        n = len(data_cloud.waitingDelay)
        x = np.mean(data_cloud.waitingDelay)

        # append delays to list
        xj.append(data_cloud.waitingDelay)
        x = np.mean(data_cloud.waitingDelay)
        x_tr = np.mean(data_cloud.waitingDelay[TRANSIENT_THRESHOLD:])
        X.append(x)
        X_transient.append(x_tr)
    
    X_mean = np.mean(X)
    S = np.std(X)
    X_mean_tr = np.mean(X_transient)
    S_tr = np.std(X_transient)
    print(f'Average delay = {X_mean} +- {3.090 * S / np.sqrt(num_sim)} (confidence 99.8%)')
    print(f'Average delay (without transient)= {X_mean_tr} +- {3.090 * S_tr / np.sqrt(num_sim)} (confidence 99.8%)')
    
    # reduce lenghts of delay lists among simulations
    lens = []
    for i in xj:
        lens.append(len(i))
    min_len = min(lens)
    xj_new = []
    for i in xj:
        xj_new.append(i[:min_len])
    xj = xj_new

    # compute delay averages across simulatios
    XJ = np.zeros(min_len) # contains the averages of delays for each packet
    for xx in xj:
        XJ += np.array(xx)
    XJ /= num_sim

    # compute xk and Rk
    x = np.mean(XJ)
    xk_list = []
    Rk = []
    for k in range(n):
        xk = np.mean(XJ[k:])
        xk_list.append(xk)
        Rk.append((xk - x) / x)

    # rolling mean and variance
    rolling_mean = []
    rolling_var = []
    for i in range(1,n):
        mean = np.mean(data_cloud.waitingDelay[:i])
        var = np.std(data_cloud.waitingDelay[:i])
        rolling_mean.append(mean)
        rolling_var.append(var)
    
    # plot last simulation delay
    plt.fill_between(np.linspace(0,n,n-1),
                     (np.array(rolling_mean[:n])+2*np.array(rolling_var[:n])),
                     (np.array(rolling_mean[:n])-2*np.array(rolling_var[:n])),
                     alpha=0.5, color='lightcoral', label='Rolling standard deviation')
    plt.plot(data_cloud.waitingDelay[0:n], label='Waiting delay')
    plt.plot(rolling_mean[:n], '--', label='Rolling mean', c='red')
    plt.axvline(x=TRANSIENT_THRESHOLD, color='orange', linestyle='-.', 
                label='Transient threshold')
    plt.legend()
    plt.grid()
    plt.xlabel("Packets")
    plt.ylabel("Waiting Delay [ms]")
    plt.title('Waiting delay over one simulation')
    plt.show()

    # Plot xk coefficent
    plt.plot(xk_list, label='xk')
    plt.plot(np.ones(min_len) * x, '--', label='Mean')
    plt.plot(np.ones(min_len) * np.mean(XJ[TRANSIENT_THRESHOLD:]), '--', 
             label='Mean (no transient)')
    plt.axvline(x=TRANSIENT_THRESHOLD, color='orange', linestyle='-.', 
                label='Transient threshold')
    plt.grid()
    plt.legend()
    plt.xlabel("Packets")
    plt.ylabel("xk")
    plt.title('Average xk averaged over 100 simulations')
    plt.show()


