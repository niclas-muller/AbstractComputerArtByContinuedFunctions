import random
import numpy as np

def getRandomFunction(numFuncs):
    listOfFuncAtoms = ['add', 'mul', 'pow', 'log', 'sin']
    listOfParameterfulFuncAtoms = ['add', 'mul', 'pow']
    randomScale = 1

    func = ''
    for funcAtomCount in range(numFuncs):
        funcAtom = random.choice(listOfFuncAtoms)
        if funcAtom in listOfParameterfulFuncAtoms:
            r = randomScale*(2*np.random.rand(2)-1)
            p = r[0]+1.j*r[1]
            func += f'{funcAtom}:{p}_'
        else:
            func += f'{funcAtom}_'
    return func[:-1]
