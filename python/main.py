import numpy as np
import matplotlib.pyplot as plt
from shanks import ShanksConverge
from funcGen import FuncGen 
from lib import getRandomFunction
from colorScheme import getColorMap
from tqdm import tqdm
import time
import warnings
warnings.filterwarnings('ignore')

class ContinuedFunctionArtFrame():
    # For a given function, center point, extent and resolution, compute the frame
    def __init__(self, function, center, extent, resolution):
        self.function = FuncGen(function).func
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

class ContinuedFunctionArtWalk():
    def __init__(self):
        pass

class ContinuedFunctionArtZoom():
    def __init__(self):
        pass

def fillBestOfDir():
    cmap = getColorMap()
    path = '../images/bestOf/'
    center = (0,0)
    extent = 1
    resolution = 100
    for _ in tqdm(range(30)):
        #fname = f'frame_{str(time.ctime()).replace(' ','_')}_.png'
        fname = f'sample_{_}.png'
        function = getRandomFunction(np.random.randint(3,20))
        frame = ContinuedFunctionArtFrame(function, center, extent, resolution).frame
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

fillBestOfDir()
