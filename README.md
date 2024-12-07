#A software to find a numerical solution for the 1D heat transfer problem

Weak Form Derivation:

![weakform](project2/Weak_Form_Derivation.jpg)

I used this derivation to help create the algorithms to solve the problem numerically.
Within the project2 folder are two files
  project2_BE.py
    This is the backwards euler method aproach to the problem
  project2_FE.py
    This is the Forward euler method aproach to the problem

Forward Euler
Changing timestep


![e1](project2/plots/FE_Solution_T=1.0_nt=551_N=11.png)
As can be seen above, the Forward Euler solution was unstable for dt=1/551 and N=11.

By reducing the time step, we can begin to get more accurate solutions:
![e1](project2/plots/FE_Solution_T=1.0_nt=561_N=11.png)

If we reduce the timestep further, we see the FE solution converges closer to the real solution:
![e1](project2/plots/FE_Solution_T=1.0_nt=571_N=11.png)

For N=11, the Forward Euler method begins to fail for timesteps greater than 1/561.

Keeping the timestep constant at 1/551, we tried increasing the number of nodes:
![e1](project2/plots/FE_Solution_T=1.0_nt=551_N=10.png)
![e1](project2/plots/FE_Solution_T=1.0_nt=551_N=9.png)
![e1](project2/plots/FE_Solution_T=1.0_nt=551_N=8.png)
![e1](project2/plots/FE_Solution_T=1.0_nt=551_N=5.png)


Backwards Euler method
