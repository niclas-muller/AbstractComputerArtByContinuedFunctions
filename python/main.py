from lib import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import os

class Draw():

    '''
        Overall class for drawing art: be it single frames, walks, zooms, etc.
    '''

    def __init__(self,
                 mode,
                 center,
                 extent,
                 resolution,
                 minFuncAtoms,
                 maxFuncAtoms,
                 numberOfSamples = 100,
                 numberOfTops = 30,
                 colors=None):

        if colors:
            self.cmap = getColorMap(colors)
        else:
            self.cmap = getColorMap()

        match mode:
            case 'bestOf':
                self.drawBestOf(center,
                                extent,
                                resolution,
                                numberOfSamples,
                                minFuncAtoms,
                                maxFuncAtoms,
                                numberOfTops)
            case _:
                raise NameError(f'Unknown mode {mode}')

    def drawBestOf(self,
                   center,
                   extent,
                   resolution,
                   numberOfSamples,
                   minFuncAtoms,
                   maxFuncAtoms,
                   numberOfTops):

        path = createNewBestOfDir()

        for _ in tqdm(range(numberOfSamples)):
            fname = f'sample_{_}.png'
            function = encodeRandomFunction(np.random.randint(minFuncAtoms,maxFuncAtoms))
            frame = Frame(function, center, extent, resolution).frame
            fig, ax = plt.subplots(1)
            ax.imshow(frame,
                      cmap = self.cmap,
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

        cleanUpBestOfDir(path,numberOfTops)

center = (0,0)
extent = 2
resolution = 200
minFuncAtoms = 2
maxFuncAtoms = 10

Draw('bestOf',center,extent,resolution,minFuncAtoms,maxFuncAtoms)
