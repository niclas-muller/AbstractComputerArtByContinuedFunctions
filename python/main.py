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
                 function=None,
                 numberOfSamples=100,
                 numberOfTops=30,
                 zoomFactor=0.95,
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
                              zoomFactor,
                              zoomInto=function)
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

        path = createNewDir('bestOf')

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
                 zoomFactor,
                 zoomInto=None):

        path = createNewDir('zoom')

        if not zoomInto:
            while True:
                function = encodeRandomFunction(np.random.randint(minFuncAtoms,maxFuncAtoms))
                fname = 'sample_0.png'
                drawFrame(function, center, extent, resolution, self.cmap, path, fname)
                goodExample = input('Good example? (y/n): ')
                if goodExample == 'y':
                    break
        else:
            function = zoomInto

        frames = []
        for _ in tqdm(range(numberOfSamples)):
            fname = f'sample_{_}.png'
            drawFrame(function, center, extent, resolution, self.cmap, path, fname)
            extent = extent*zoomFactor
            frames.append(f'{path}{fname}')

        makeGif(path,frames)

        for fname in [fname for fname in os.listdir(path) if 'png' in fname]:
            os.remove(f'{path}/{fname}')

        try:
            zoomCount = max([int(fname.split('_')[1].split('.')[0]) for fname in os.listdir('../images/zooms')]) + 1
        except IndexError:
            zoomCount = 0

        os.rename(f'{path}/zoom.gif',f'../images/zooms/zoom_{zoomCount}.gif')
        os.rmdir(path)

center = (0,0)
extent = 20
resolution = 250
minFuncAtoms = 2
maxFuncAtoms = 10
numberOfSamples = 360 # 360 for zooms and orbits
testPath = '../images/bestOf/frame_41.png'
function = getFunctionFromFrame(testPath)
print(function)

Draw('zoom',
     center,
     extent,
     resolution,
     minFuncAtoms,
     maxFuncAtoms,
     numberOfSamples=numberOfSamples,
     function=function)
