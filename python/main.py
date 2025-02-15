from lib import *
from tqdm import tqdm

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
                 zoomFactor = 0.99,
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
            case 'zoom':
                self.drawZoom(center,
                              extent,
                              resolution,
                              numberOfSamples,
                              minFuncAtoms,
                              maxFuncAtoms,
                              zoomFactor)
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
            drawFrame(function, center, extent, resolution, self.cmap, path, fname)

        cleanUpBestOfDir(path,numberOfTops)

    def drawZoom(self,
                 center,
                 extent,
                 resolution,
                 numberOfSamples,
                 minFuncAtoms,
                 maxFuncAtoms,
                 zoomFactor):

        path = createNewZoomDir()
        while True:
            function = encodeRandomFunction(np.random.randint(minFuncAtoms,maxFuncAtoms))
            fname = 'sample_0.png'
            drawFrame(function, center, extent, resolution, self.cmap, path, fname)
            goodExample = input('Good example? (y/n): ')
            if goodExample == 'y':
                break

        for _ in tqdm(range(numberOfSamples)):
            fname = f'sample_{_}.png'
            drawFrame(function, center, extent, resolution, self.cmap, path, fname)
            extent = extent*zoomFactor

        makeGif(path)

center = (0,0)
extent = 20
resolution = 50
minFuncAtoms = 6
maxFuncAtoms = 9
numberOfSamples = 500

Draw('zoom',center,extent,resolution,minFuncAtoms,maxFuncAtoms,numberOfSamples)
