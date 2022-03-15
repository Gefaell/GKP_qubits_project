import numpy as np
import matplotlib.pyplot as plt
import strawberryfields as sf
import strawberryfields.ops as ops
import tensorflow as tf
# from qutip import wigner, Qobj, wigner_cmap, fidelity
from tqdm import tqdm
from cutoff_opt import min_cutoff
# import matplotlib as plt
# from matplotlib import cm
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# from  import target_dm, cutoff



from target import target
# print('cutoff of gkp target is =', cutoff)
#%%




def newcost(a, s, db):
    target_dm, cutoff = target(db)
    print('cutoff=', cutoff)
    prog = sf.Program(2)
    
    with prog.context as q:
        ops.Catstate(a) | q[0]
        ops.Catstate(a) | q[1]
        ops.Sgate(s) | q[0]
        ops.Sgate(s) | q[1]
        ops.BSgate() | (q[0], q[1])
        ops.MeasureHomodyne(np.pi/2, select=0.0) | q[0]
    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim":cutoff})
    state = eng.run(prog).state
    
    dm = state.reduced_dm(1)
    # dm_q = Qobj(dm)
    
    
    # target_dm_q = Qobj(target_dm)

    # fid = fidelity(dm_q, target_dm_q)
    trace_dist = 0.5*np.trace(np.abs(dm - target_dm))
    return trace_dist
        




def acceptancefunction(dE, T):
    
    
    if dE <= 0.0:
        return 1
    
    print(f'dE = {dE}')
    print(f' Probability of still accepting = ', np.exp(-1.0 * dE/T))
    
    if np.random.uniform(0,1,1) < np.exp(-1.0 * dE/T): 
        return 1
    return 0

def ProposalFunction(u,sigma_a,sigma_s, sigma_db):
    x = np.random.normal(0.0, sigma_a) + u[0]
    y = np.random.normal(0.0, sigma_s) + u[1]
    z = np.random.normal(0.0, sigma_db) + u[2]
    return np.array([x,y,z])

def runchain3d(f, a, s, db, sigma_a, sigma_s, sigma_db):
    T = 0.03
    temps = np.arange(T,0,-0.005)
    iterations = 1000
    
    values = [a,s,db]
    
    listofvalues = []
    cost_progress = []
    
    for T in temps:
        zeros = np.zeros((iterations+1,len(values)))
        zeros[0,:] = values 

        print('Currently runnin on temp =', T)
        for j in range(iterations):
            params_now = zeros[j,:]
            print(params_now)
            # print(len(params_now))
            params_next = ProposalFunction(params_now, sigma_a, sigma_s, sigma_db)
            while params_next[0] < 0:
                newchoice =  ProposalFunction(params_now, sigma_a, sigma_s, sigma_db)
                params_next[0] = newchoice[0]
            while params_next[1] < 0:
                newchoice =  ProposalFunction(params_now, sigma_a, sigma_s, sigma_db)
                params_next[1] = newchoice[1]
            while params_next[2] < 0 or params_next[2] >16:
                newchoice =  ProposalFunction(params_now, sigma_a, sigma_s, sigma_db)
                params_next[2] = newchoice[2]
            cost_now = f(params_now[0],params_now[1], params_now[2])
            # print(unext)
            # print(type(unext))
            cost_next = f(params_next[0],params_next[1], params_next[2])
            dE = cost_next - cost_now
            
            acceptstep = acceptancefunction(dE,T)
            if acceptstep == 1:
                zeros[j+1,:] = params_next
            if acceptstep == 0:
                zeros[j+1,:] = params_now
            cost_progress.append(cost_now)
        values = zeros[-1,:]
        listofvalues.append(zeros)
        
    return listofvalues, cost_progress

#%%
t,cost_progress = runchain3d(newcost, 3, 0.2, 10, 0.2, 0.2, 1)
#%%


np.save('anneal3D_0.3_0.0_-0.005_100', t)
np.save('cost_prog3D_0.3_0.0,-0.05,100', cost_progress)
#%%
t = np.load('anneal_0.3_0.0_-0.005_100',allow_pickle=True)
cost_progress = np.load('cost_prog_0.3_0.0,-0.05,100', allow_pickle=True)
#%%

lists = []
for i in range(len(t)):
    lists.append(t[i])

anneal= np.vstack((lists))
#%%
a_vals = anneal[:,0]
plt.plot(np.arange(0,len(anneal),1),anneal[:,0])
plt.ylabel(r'$\alpha$')
plt.xlabel(r'Iteration number')
#%%

s_vals = anneal[:,1]
plt.plot(np.arange(0,len(anneal),1),anneal[:,1])
plt.ylabel(r'$s$')
plt.xlabel(r'Iteration number')

#%%

db_vals = anneal[:,1]
plt.plot(np.arange(0,len(anneal),1),anneal[:,2])
plt.ylabel(r'$db$')
plt.xlabel(r'Iteration number')
#%%
plt.plot(range(len(cost_progress)), cost_progress)
plt.xlabel(r'Iterations Number')
plt.ylabel(r'Trace Distance')

#%%
for i in range(len(cost_progress)):
    if abs(cost_progress[i] - 0.07668706570657034) <0.0001:
        optimal_i = i
optimal_val = [a_vals[optimal_i],s_vals[optimal_i]]
# print(f'Optimal vals = {optimal_val}')
# print('optimal cost =', newcost(*optimal_val))