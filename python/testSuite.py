import numpy as np
import matplotlib.pyplot as plt
from lib import *
import cProfile

# Test encode of random function

print('Testing random function encoder:\n')
for _ in range(4):
    encodedFunction = encodeRandomFunction(3+_, rndParamRange=1)
    print(f'Encoded function with {3+_} elements: \n')
    print(f'{encodedFunction}\n')

# Test decode of function

print('Testing decoding of encoded function:\n')

rnd_real_0, rnd_imag_0, rnd_real_1, rnd_imag_1 = 2*np.random.rand(4) - 1
param_0 = rnd_real_0 + 1.j*rnd_imag_0
param_1 = rnd_real_1 + 1.j*rnd_imag_1

low = -1
hgh = 1
resolution = 300
x_arr = np.linspace(low, hgh, resolution)

f = decodeFunction(f'pow:0.5_mul:{param_1}_add:{param_0}_log_sin')

y_exact = np.sin(np.log(param_0 + param_1*np.sqrt(x_arr+0.j)))

y_test = np.vectorize(f)(x_arr)

fig, ax = plt.subplots(1)
ax.plot(x_arr, abs(y_exact - y_test))
ax.set_xlabel('x')
ax.set_ylabel(r'abs(y_exact - y_test)')
ax.set_title(f'Total deviation: {np.sum(abs(y_exact - y_test))}')
plt.show()
plt.close(fig)

# Test shanks convergence

print('Testing convergence of shanks procedure:\n')

numOfFuncAtoms = 6
func = decodeFunction(encodeRandomFunction(numOfFuncAtoms))
z_real, z_imag = 2*np.random.rand(2)-1
z = z_real + 1.j*z_imag
plainSteps = 500

full = [z]
for _ in range(plainSteps):
    full.append(func(full[-1]))

low = min(np.min(np.real(full)),np.min(np.imag(full)))
hgh = max(np.max(np.real(full)),np.max(np.imag(full)))

shnks = ShanksConverge(z,func)

rLim = np.real(shnks.limit)
iLim = np.imag(shnks.limit)

fig, axes = plt.subplots(ncols=3)

axes[0].set_title('Full plain iteration')
axes[0].plot(np.real(full))
axes[0].plot(np.imag(full))

axes[1].set_title('Plain iteration')
axes[1].plot(np.real(shnks.shanksLadder[0]))
axes[1].plot(np.imag(shnks.shanksLadder[0]))

axes[2].set_title('Best estimates')
axes[2].plot(np.real(shnks.bestEstimates))
axes[2].plot(np.imag(shnks.bestEstimates))

for ax in axes:
    ax.set_ylim(low,hgh)
    ax.axhline(y = rLim, ls = 'dotted')
    ax.axhline(y = iLim, ls = 'dotted')

plt.tight_layout()
plt.show()
plt.close(fig)

# Profiling frame generation

print('Profiling frame generation:\n')

center = (-1,2)
extent = 1
resolution = 100
a = 0.6889056865544987-0.000507424433446868j 
b = 0.027905233067976765-0.5703520544167373j
func = f'sin_sin_mul:{a}_add:{b}_log'

with cProfile.Profile() as pr:
    frame = Frame(func, center, extent, resolution)
    pr.print_stats(sort='cumtime')
