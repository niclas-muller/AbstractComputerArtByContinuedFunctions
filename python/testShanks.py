import numpy as np
import matplotlib.pyplot as plt
from shanks import ShanksConverge
from tqdm import tqdm

randoms = 2*(np.random.rand(6)-0.5)
a = randoms[0] + 1.j*randoms[1]
b = randoms[2] + 1.j*randoms[3]
z = randoms[4] + 1.j*randoms[5]
func = lambda z: np.log(a+b*np.sin(z))

full = [z]
for _ in range(1000):
    full.append(func(full[-1]))

low = min(np.min(np.real(full)),np.min(np.imag(full)))
hgh = max(np.max(np.real(full)),np.max(np.imag(full)))

shnks = ShanksConverge(z,func)

rLim = np.real(shnks.limit)
iLim = np.imag(shnks.limit)

fig, axes = plt.subplots(ncols=3)
axes[0].set_title('full plain iteration')
axes[0].plot(np.real(full))
axes[0].plot(np.imag(full))
axes[0].set_ylim(low,hgh)
axes[0].axhline(y=rLim)
axes[0].axhline(y=iLim)

axes[1].set_title('plain iteration')
axes[1].plot(np.real(shnks.shanksLadder[0]))
axes[1].plot(np.imag(shnks.shanksLadder[0]))
axes[1].set_ylim(low,hgh)
axes[1].axhline(y=rLim)
axes[1].axhline(y=iLim)

axes[2].set_title('best estimates')
axes[2].plot(np.real(shnks.bestEstimates))
axes[2].plot(np.imag(shnks.bestEstimates))
axes[2].set_ylim(low,hgh)
axes[2].axhline(y=rLim)
axes[2].axhline(y=iLim)


plt.tight_layout()
plt.show()

