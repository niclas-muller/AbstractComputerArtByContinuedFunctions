import numpy as np
import matplotlib.pyplot as plt
from shanks import ShanksConverge
from tqdm import tqdm

class ContinuedFunctionArtFrame():
    # For a given function, center point, extent and resolution, compute the frame
    def __init__(self, function, center, extent, resolution, grid=None):
        self.function = function
        if grid:
            self.grid = grid
        else:
            self.constructGrid(center, extent, resolution)
        self.computeFrame()

    def constructGrid(self, center, extent, resolution):
        lowerLeftCorner = (center[0] - 0.5*extent, center[1] - 0.5*extent)
        upperRghtCorner = (center[0] + 0.5*extent, center[1] + 0.5*extent)
        xGrid = np.linspace(lowerLeftCorner[0], upperRghtCorner[0], num=resolution)
        yGrid = np.linspace(lowerLeftCorner[1], upperRghtCorner[1], num=resolution)
        self.grid = np.empty((resolution, resolution), dtype = np.complex128)
        for xCount, x in enumerate(xGrid):
            for yCount, y in enumerate(yGrid):
                self.grid[xCount,yCount] = x + 1.j*y

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

center = (0,0)
extent = 1
resolution = 300
for funcType in tqdm(['LogOfCube','LogOfLin','LogOfLog','LogOfSine','LogOfSquare','LogOfRoot']):
    for _ in range(20):
        randoms = 2*(np.random.rand(4)-0.5)
        a = randoms[0] + 1.j*randoms[1]
        b = randoms[2] + 1.j*randoms[3]

        if funcType == 'LogOfCube':
            func = lambda z: np.log(a+b*z*z*z)
        if funcType == 'LogOfLin':
            func = lambda z: np.log(a+b*z)
        if funcType == 'LogOfLog':
            func = lambda z: np.log(a+b*np.log(z))
        if funcType == 'LogOfSine':
            func = lambda z: np.log(a+b*np.sin(z))
        if funcType == 'LogOfSquare':
            func = lambda z: np.log(a+b*z*z)
        if funcType == 'LogOfRoot':
            func = lambda z: np.log(a+b*np.sqrt(z))
            
        frame = ContinuedFunctionArtFrame(func, center, extent, resolution).frame
        fig, ax = plt.subplots(1)
        ax.imshow(frame,origin='lower',cmap='twilight')
        ax.set_axis_off()
        fig.savefig(f'../images/samples/{funcType}/sample_{_}.png', bbox_inches='tight',pad_inches=0)
        fig.close()
