import numpy as np
#import warnings
#warnings.filterwarnings('error')

class ShanksConverge():
    # Compute the limit of a sequence defined by continued application of the function "function" to the starting value initVal using all available shanks transforms

    def __init__(self,initVal,function):
        self.function = function
        self.shanksLadder = [[initVal]]
        self.totalIterations = 0
        self.iterateBase()
        self.iterateBase()
        self.shanksLevel = 0
        self.isConverged = False
        self.maxIterations = 100
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
