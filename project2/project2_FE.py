import numpy as np
import matplotlib.pyplot as plt
save_plots = True
# Parameters and user defined values
N=8
t0=0
tf=1.0
dt=1.0/551.0
x0=0
xf=1.0

#initial u
def u_init(x):
    return np.sin(np.pi*x)
nt=(tf-t0)/dt

#Dir. BC's
BC_nodes=[0,N-1] #global node numbers where BCs are applied
BC_vals=[0,0]

#Number of elems.
Ne=N-1

#Right hand side
def f(x,t): #x:1d, t:2d
    return (np.pi**2-1)*np.exp(-t)*np.sin(np.pi*x)
    
#exact solution
def u_exact(x_vals,t): 
    return np.exp(-t) * np.sin(np.pi * x_vals)
    
#uniform grid/connectivity map
Ne= N - 1
h=(xf - x0)/(N-1)
x = np.zeros(N)
iee = np.zeros((Ne,2))

for i in range(Ne):
    x[i] = x0 + (i)*h
    iee[i][0] = i
    iee[i][1] = i + 1
x[N-1] = xf

#xi, phis, and dphis for quadrature
xi=np.array([1/np.sqrt(3),-1/np.sqrt(3)])
def phis(xi):
    return np.array([(1 - xi) / 2, (1 + xi) / 2])
dphis= np.array([-1/2, 1/2]) #constant value

#start of K and M calculations
# Initialization
K = np.zeros((N,N))
M= np.zeros((N,N))
klocal = np.zeros((2,2))
mlocal= np.zeros((2,2))

f_local = np.zeros(2)
for k in range(Ne):
    #Local K and M calc.
    klocal = np.zeros((2,2))
    mlocal= np.zeros((2,2))
    for l in range(2):
        phis_xi = phis(xi[l])
        mlocal += h/2*np.outer(phis_xi, phis_xi)   #weights are 1 for 2d quadrature
        klocal += (2/h)*np.outer(dphis, dphis)
    #FE assembly
    for l in range(2):
        global_node1 = int(iee[k][l])
        #F[global_node1] += f_local[l]
        for m in range(2):
            global_node2 = int(iee[k][m])
            K[global_node1][global_node2] += klocal[l][m]
            M[global_node1][global_node2] += mlocal[l][m]

#Calculating inverse M
M_inv = np.linalg.inv(M)

#applying our dir. boundary conditions:
for i, bc_node in enumerate(BC_nodes):
    K[bc_node,:] = BC_vals[i]
    K[:,bc_node] = BC_vals[i]
    M[bc_node,:] = BC_vals[i]
    M[:,bc_node] = BC_vals[i]
    K[bc_node, bc_node]=1
    
#Looping through time steps
u=u_init(x)
f_local=np.zeros(2)
F=np.zeros(N)
for n in range(int(nt)):
    F=np.zeros(N) #need to reset every timestep to stop solution from blowing up
    ctime=t0+n*dt
    for k in range(Ne):
        flocal=np.zeros(2)
        # local elem calc.
        for l in range(2):
            phis_xi = phis(xi[l])
            x_curr=x0+iee[k][l]*h
            f_local[l] = np.sum((h/2)*f(x_curr, ctime) * phis_xi)
        for i in range(2):
            global_node1 = int(iee[k][i])
            F[int(global_node1)] += f_local[i]
#applying our dir. BCs to F
    for i, bc_node in enumerate(BC_nodes):
        F[bc_node]=BC_vals[i]
        
#finally, we go to the next time step
    u = u-dt*M_inv@K@u + dt*M_inv@F

#Output

plt.plot(x, u, label= 'FE Aproximation', color='blue')
x_test=np.linspace(x[0],x[-1],100)
final_exact=(np.exp(-tf)*np.sin(np.pi*x_test))
plt.plot(x_test, final_exact, label= 'Exact Solution', color='red')
plt.title(f"Forward Euler FE solution at T ={tf} nt={int(nt)} N={N}")
plt.legend()
#plt.show()
#save plots
if save_plots:
    filename = f"FE_Solution_T={tf:.1f}_nt={int(nt)}_N={N}.png"
    plt.savefig(f"./project2/plots/{filename}")
    print(f"Plot saved to {filename}")
else:
    plt.show()