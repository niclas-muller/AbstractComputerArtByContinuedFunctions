from lib import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import os

class Draw():

    '''
        Overall class for drawing art: be it single frames, walks, zooms, etc.
    '''

    def __init__(self,mode,*args):
        self.cmap = getColorMap()
        match mode:
            case 'bestOf':
                self.drawBestOf(args)
            case _:
                raise NameError(f'Unknown mode {mode}')

    def drawBestOf(self,args):
        path = '../images/bestOf/'
        existingFiles = os.listdir(path)
        maxFileIndex = max([int(fname.split('_')[1].split('.')[0]) for fname in existingFiles]) 
        center = (0,0)
        extent = 2
        resolution = 500

        for _ in tqdm(range(maxFileIndex + 1,maxFileIndex + 100)):
            fname = f'sample_{_}.png'
            function = encodeRandomFunction(np.random.randint(3,20))
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

Draw('bestOf',{'param1': 1, 'param_2': 2})
