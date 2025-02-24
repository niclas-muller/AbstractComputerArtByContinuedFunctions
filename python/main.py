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
                 numberOfSamples,
                 minFuncAtoms=2,
                 maxFuncAtoms=10,
                 function=None,
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
                                maxFuncAtoms)
                                
            case 'zoom':
                self.drawZoom(center,
                              extent,
                              resolution,
                              numberOfSamples,
                              zoomFactor,
                              function)

            case 'orbit':
                self.drawOrbit(center,
                               extent,
                               resolution,
                               numberOfSamples,
                               function)
            case _:
                raise NameError(f'Unknown mode *{mode}*')

    def drawBestOf(self,
                   center,
                   extent,
                   resolution,
                   numberOfSamples,
                   minFuncAtoms,
                   maxFuncAtoms):

        path = createNewDir('bestOf')

        for _ in tqdm(range(numberOfSamples)):
            fname = f'sample_{_}.png'
            function = encodeRandomFunction(np.random.randint(minFuncAtoms,maxFuncAtoms))
            drawFrame(function, center, extent, resolution, self.cmap, path, fname)

        cleanUpBestOfDir(path)

    def drawZoom(self,
                 center,
                 extent,
                 resolution,
                 numberOfSamples,
                 zoomFactor,
                 function):

        path = createNewDir('zoom')

        frames = []
        for _ in tqdm(range(numberOfSamples)):
            fname = f'sample_{_}.png'
            drawFrame(function, center, extent, resolution, self.cmap, path, fname)
            extent = extent*zoomFactor
            frames.append(f'{path}{fname}')

        makeGif(path,frames,zoom)

        for fname in [fname for fname in os.listdir(path) if 'png' in fname]:
            os.remove(f'{path}/{fname}')

        try:
            zoomCount = max([int(fname.split('_')[1].split('.')[0]) for fname in os.listdir('../images/zooms')]) + 1
        except IndexError:
            zoomCount = 0

        os.rename(f'{path}/zoom.gif',f'../images/zooms/zoom_{zoomCount}.gif')
        os.rmdir(path)

    def drawOrbit(self,
                  center,
                  extent,
                  resolution,
                  numberOfSamples,
                  function):

        path = createNewDir('orbit')

        frames = []
        for _ in tqdm(range(numberOfSamples)):
            rotateBy = np.exp(1.j*(_/numberOfSamples)*(2*np.pi))
            rotatedFunc = rotateFunctionForOrbit(function, rotateBy)
            fname = f'sample_{_}.png'
            drawFrame(rotatedFunc, center, extent, resolution, self.cmap, path, fname)
            frames.append(f'{path}{fname}')

        makeGif(path,frames,'orbit')

        for fname in [fname for fname in os.listdir(path) if 'png' in fname]:
            os.remove(f'{path}/{fname}')
        
        try:
            orbitCount = max([int(fname.split('_')[1].split('.')[0]) for fname in os.listdir('../images/orbits')]) + 1
        except ValueError:
            orbitCount = 0

        os.rename(f'{path}/orbit.gif',f'../images/orbits/orbit_{orbitCount}.gif')
        os.rmdir(path)

center = (0,0)
extent = 1
resolution = 400
minFuncAtoms = 2
maxFuncAtoms = 10
numberOfSamples = 360 # 360 for zooms and orbits
testPath = '../images/bestOf/frame_28.png'
function = getFunctionFromFrame(testPath)

Draw('orbit',
     center,
     extent,
     resolution,
     #minFuncAtoms,
     #maxFuncAtoms,
     numberOfSamples,
     function=function)
