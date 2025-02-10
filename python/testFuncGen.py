import numpy as np
import matplotlib.pyplot as plt
from funcGen import FuncGen
from tqdm import tqdm

r = 2*np.random.rand(4)-1
c0 = r[0]+1.j*r[1]
c1 = r[2]+1.j*r[3]

x = np.linspace(-1,1,300)

f = FuncGen(f'pow:0.5_mul:{c1}_add:{c0}_log_sin').func

y_exact = np.sin(np.log(c0 + c1*np.sqrt(x+0.j)))

y_test = np.vectorize(f)(x)

plt.plot(x,abs(y_exact-y_test))
plt.show()
