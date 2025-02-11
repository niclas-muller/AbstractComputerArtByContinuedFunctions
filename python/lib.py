import random
import numpy as np
import matplotlib.colors as col
import time
import warnings
warnings.filterwarnings('ignore')

def encodeRandomFunction(numOfFuncAtoms, rndParamRange=1):

    '''
        Given a predefined number of function atoms, create a random sequence encoding
        a function that can be interpreted by decodeFunction
    '''

    listOfFuncAtoms = ['add', 'mul', 'pow', 'log', 'sin']
    listOfParamfulFuncAtoms = ['add', 'mul', 'pow']

    encodedFunc = ''
    for funcAtomCount in range(numOfFuncAtoms):
        funcAtom = random.choice(listOfFuncAtoms)
        if funcAtom in listOfParamfulFuncAtoms:
            rnd_real, rnd_imag = rndParamRange*(2*np.random.rand(2)-1)
            param = rnd_real + 1.j*rnd_imag
            encodedFunc += f'{funcAtom}:{param}_'
        else:
            encodedFunc += f'{funcAtom}_'
    return encodedFunc[:-1]

def createFuncAtom(funcElem):

    '''
        Helper for decodeFunction: given a function element of the type:
        funcName:param, return a lambda function that performs the corresponding 
        operation on the input
    '''

    funcElem = funcElem.split(':')
    if len(funcElem) == 2:
        param = np.complex128(funcElem[1])
    match funcElem[0]:
        case 'mul':
            return (lambda x: x*param)
        case 'add':
            return (lambda x: x + param)
        case 'pow':
            return (lambda x: x**param)
        case 'log':
            return (lambda x: np.log(x))
        case 'sin':
            return (lambda x: np.sin(x))
        case _:
            raise NameError(f'Undefined function atom {funcElem}')

def decodeFunction(encodedFunction):

    '''
        Given an ordered sequence of function types, this function returns the decoded
        function that corresponds to that sequence. Available functions are:
            - mul: multiplication by constant (needs to be passed)
            - add: addition with constant (needs to be passed)
            - pow: raise to power (needs to be passed)
            - log: compute natural log
            - sin: compute sin

        Example: in order to encode the function sin(log(c0 + c1*sqrt(z))) we write:
        seq = 'pow:0.5_mul:c1_add:c0_log_sin', so functional elements are separated by
        underscores, parameterized functions are appended by the respective parameter 
        after a colon.
    '''

    funcPlan = []
    for funcElem in encodedFunction.split('_'):
        funcPlan.append(createFuncAtom(funcElem))

    def chainedFunc(x):
        x += 0.j
        for f in funcPlan:
            x = f(x)
        return x

    return chainedFunc

class ShanksConverge():

    ''' 
        Compute the limit of a sequence defined by continued application 
        of the function "function" to the starting value initVal 
        using all available shanks transforms
    '''

    def __init__(self,initVal,function):
        self.function = function
        self.shanksLadder = [[initVal]]
        self.totalIterations = 0
        self.iterateBase()
        self.iterateBase()
        self.shanksLevel = 0
        self.isConverged = False
        self.maxIterations = 50
        self.convergenceThreshold = 1e-3
        self.bestEstimates = []
        self.iterate()

    def iterateBase(self):
        # apply the function to the last element of the base sequence (without any shanks transforms)
        oldVal = self.shanksLadder[0][-1]
        nxtVal = self.function(oldVal)
        self.shanksLadder[0].append(nxtVal)
        self.totalIterations += 1

    def _shanks(self,tmp):
        d1 = tmp[2] - tmp[1]
        d0 = tmp[1] - tmp[0]
        corr = d1*d1/(d1 - d0)
        return tmp[2] - corr

    def iterateShanks(self):
        for depth in range(self.shanksLevel):
            tmp = self.shanksLadder[depth][-3:]
            res = self._shanks(tmp)
            self.shanksLadder[depth + 1].append(res)

    def increaseShanksLevel(self):
        # increase the shanks depth by one level, compute the first element in the deepest level
        self.shanksLadder.append([])
        self.shanksLevel += 1
        tmp = self.shanksLadder[-2][-3:]
        res = self._shanks(tmp)
        self.shanksLadder[-1].append(res)

    def assessConvergence(self):
        # add the latest approximant to the list of limits and check if convergence has been achieved
        try:
            self.bestEstimates.append(self.shanksLadder[-1][-1])
            diff1 = abs(self.bestEstimates[-1] - self.bestEstimates[-2])
            diff2 = abs(self.bestEstimates[-2] - self.bestEstimates[-3])
            if diff1 < self.convergenceThreshold and diff2 < self.convergenceThreshold:
                self.isConverged = True
                self.limit = self.bestEstimates[-1]
        except IndexError:
            pass

    def iterate(self):
        while not self.isConverged and self.totalIterations < self.maxIterations:
            self.increaseShanksLevel()
            self.iterateBase()
            self.iterateShanks()
            self.iterateBase()
            self.iterateShanks()
            self.assessConvergence()

class Frame():

    # For a given function, center point, extent and resolution, compute the frame

    def __init__(self, function, center, extent, resolution):
        self.function = decodeFunction(function)
        self.constructGrid(center, extent, resolution)
        self.computeFrame()

    def constructGrid(self, center, extent, resolution):
        lowerLeftCorner = (center[0] - 0.5*extent, center[1] - 0.5*extent)
        upperRghtCorner = (center[0] + 0.5*extent, center[1] + 0.5*extent)
        xGrid = np.linspace(lowerLeftCorner[0], upperRghtCorner[0], num=resolution)
        yGrid = np.linspace(upperRghtCorner[1], lowerLeftCorner[1], num=resolution)
        X, Y = np.meshgrid(xGrid, yGrid)
        self.grid = X + 1.j*Y

    def computeFrame(self):
        
        def applyContinuedFunction(z):
            shnks = ShanksConverge(z,self.function)
            if shnks.isConverged:
                return np.angle(shnks.limit)
            else: 
                return np.nan

        vectorizedApply = np.vectorize(applyContinuedFunction)
        self.frame = vectorizedApply(self.grid)

def getColorMap(right = '#C96868', up = '#FADFA1', left = '#FFF4EA', down = '#7EACB5'):

    '''
        Given four colors, create a cyclic colormap and return it
    '''

    colors = [left,down,right,up,left]
    return col.LinearSegmentedColormap.from_list('myMap',colors,N=256,gamma=1.0)
