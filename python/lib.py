import random
import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import subprocess
import warnings
warnings.filterwarnings('ignore')

def encodeRandomFunction(numOfFuncAtoms, rndParamRange=1):

    '''
        Given a predefined number of function atoms, create a random sequence encoding
        a function that can be interpreted by decodeFunction
    '''

    listOfFuncAtoms = ['add', 'mul', 'pow', 'log', 'sin', 'tan', 'sinc', 'conj', 'mulx']
    listOfParamfulFuncAtoms = ['add', 'mul', 'pow', 'mulx']

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
            return (lambda x: np.multiply(x,param))
        case 'add':
            return (lambda x: np.add(x,param))
        case 'pow':
            return (lambda x: np.power(x,param))
        case 'log':
            return (lambda x: np.log(x))
        case 'sin':
            return (lambda x: np.sin(x))
        case 'tan':
            return (lambda x: np.tan(x))
        case 'sinc':
            return (lambda x: np.sinc(x))
        case 'conj':
            return (lambda x: np.conjugate(x))
        case 'mulx':
            return (lambda x: np.multiply(x,np.power(x,param)))
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
        self.limit = np.nan
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
                # implement option to show nan instead?
                return np.angle(shnks.bestEstimates[-1])

        vectorizedApply = np.vectorize(applyContinuedFunction)
        self.frame = vectorizedApply(self.grid)

def getColorMap(colors=('#C96868','#FADFA1','#FFF4EA','#7EACB5')):
    #Given four colors, create a cyclic colormap and return it
    right, up, left, down = colors
    colors = [left,down,right,up,left]
    return col.LinearSegmentedColormap.from_list('myMap',colors,N=256,gamma=1.0)

def drawFrame(function, center, extent, resolution, cmap, path, fname):
    frame = Frame(function, center, extent, resolution).frame
    fig, ax = plt.subplots(1)
    ax.imshow(frame,
              cmap = cmap,
              norm = 'linear',
              vmin = -np.pi,
              vmax = np.pi,
              interpolation = 'lanczos',
              origin='lower')
    ax.set_axis_off()
    fig.savefig(f'{path}{fname}',
                bbox_inches = 'tight',
                pad_inches = 0,
                metadata = {'Comment': function})
    plt.close(fig)

def createNewBestOfDir():
    runCount = 0
    path = f'../images/bestOf_{runCount}/'
    while os.path.exists(path):
        runCount += 1
        path = f'../images/bestOf_{runCount}/'
    os.makedirs(path)
    return path

def createNewZoomDir():
    runCount = 0
    path = f'../images/zoom_{runCount}/'
    while os.path.exists(path):
        runCount += 1
        path = f'../images/bestOf_{runCount}/'
    os.makedirs(path)
    return path

def cleanUpBestOfDir(path,numberOfTops):
    # load metadata of frames
    bestOfCount = path.split("_")[1][:-1]
    paths = [path + fname for fname in os.listdir(path) if '.png' in fname]
    df = []
    for p in paths:
        rawInfo = subprocess.check_output(['identify', '-verbose', p])
        rawInfo = str(rawInfo)
        rawInfo = rawInfo.replace(' ','')
        rawInfo = rawInfo.split('\\n')
        rawInfo = [{e.split(':')[0]: ':'.join(e.split(':')[1:])} for e in rawInfo if len(e.split(':')) > 1]
        info = {}
        for d in rawInfo:
            info.update(d)
        df.append(info)
    df = pd.DataFrame(df)

    # process metadata
    relevantColumns = ['min','standarddeviation','kurtosis','entropy','Colors','Comment','filename','Filesize','Pixelspersecond']
    df = df[relevantColumns]
    df = df.set_index('filename')

    # fix dtypes:
    for col in ['min', 'standarddeviation']:
        df[col] = df.apply(lambda row: float(row[col].replace(')','').split('(')[1]), axis=1)

    for col in ['kurtosis', 'entropy']:
        df[col] = df[col].astype('float')

    df.Colors = df.Colors.astype(int)
    df.Filesize = df.apply(lambda row: int(row['Filesize'].replace('B','')), axis=1)
    df.Pixelspersecond = df.apply(lambda row: float(row['Pixelspersecond'].replace('MB','')), axis=1)

    # compute ranks
    for kpi, order in [('min',True),
                       ('standarddeviation',False),
                       ('kurtosis',True),
                       ('entropy',False),
                       ('Colors',False),
                       ('Filesize',False),
                       ('Pixelspersecond',True)]:
        df[f'{kpi}_rank'] = df[kpi].rank(ascending=order)
    df['tot_rank'] = df[[col for col in df.columns if 'rank' in col]].sum(axis=1)
    df.tot_rank = df.tot_rank.rank(method='first')
    df = df.sort_values(by='tot_rank')
    df.to_excel(f'FrameOverview_{bestOfCount}.xlsx')

    # move non-top-30 into new folder (olds) and rename top-30s
    longtailPath = path+'longtail'
    if not os.path.exists(longtailPath):
        os.makedirs(longtailPath)

    toBeMoved = df.query('tot_rank > @numberOfTops').index
    for p in toBeMoved.tolist():
        os.rename(p,p.replace(f'bestOf_{bestOfCount}',f'bestOf_{bestOfCount}/longtail/'))

    toBeRenamed = df.query('tot_rank <= @numberOfTops')
    for index, row in toBeRenamed.iterrows():
        tmpPath = f'{path}tmp_{int(row["tot_rank"])}.png'
        os.rename(index,tmpPath)

    paths = [path+fname for fname in os.listdir(path) if '.png' in fname]
    for p in paths:
        os.rename(p,p.replace('tmp','sample'))

def makeGif(path):
    pass
