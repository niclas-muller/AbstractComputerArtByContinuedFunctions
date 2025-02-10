import numpy as np
import matplotlib.pyplot as plt
from shanks import ShanksConverge
from lib import getRandomFunction
from funcGen import FuncGen

func = FuncGen(getRandomFunction(11)).func
randoms = 2*np.random.rand(2)-1
z = randoms[0] + 1.j*randoms[1]
plainSteps = 1000

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
    ax.axhline(y=rLim)
    ax.axhline(y=iLim)

plt.tight_layout()
plt.show()
