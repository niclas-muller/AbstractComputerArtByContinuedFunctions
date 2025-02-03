class ShanksConverge():
    # Compute the limit of a sequence defined by continued application of the function "function" to the starting value initVal using all available shanks transforms

    def __init__(initVal,function):
        # initialize
        self.function = function
        self.shanksLadder = [[initVal]]
        self.totalIterations = 0
        self.iterateBase()
        self.iterateBase()
        self.shanksLevel = 0
        self.isConverged = False
        self.maxIterations = 100
        self.convergenceThreshold = 1e-3
        self.bestEstimates = [initVal]
        self.iterate()

    def iterateBase(self):
        # apply the function to the last element of the base sequence (without any shanks transforms)
        self.shanksLadder[0].append(function(self.shanksLadder[0][-1]))
        self.totalIterations += 1

    def iterateShanks(self):
        for depth in range(self.shanksLevel):
            tmp = self.shanksLadder[depth][-2:]
            self.shanksLadder[depth + 1].append((tmp[0]*tmp[2] - tmp[1]*tmp[1])/(tmp[0] + tmp[2] - 2*tmp[1]))

    def increaseShanksLevel(self):
        # increase the shanks depth by one level, compute the first element in the deepest level
        self.shanksLadder.append([])
        self.shanksLevel += 1
        tmp = self.shanksLadder[-2][-2:]
        self.shanksLadder[-1].append((tmp[0]*tmp[2] - tmp[1]*tmp[1])/(tmp[0] + tmp[2] - 2*tmp[1]))

    def assessConvergence(self):
        # add the latest approximant to the list of limits and check if convergence has been achieved
        self.bestEstimates.append(self.shanksLadder[-1][-1])
        if abs(self.bestEstimates[-1] - self.bestEstimates[-2]) < self.convergenceThreshold:
            self.isConverged = True
            self.limit = self.bestEstimates[-1]

    def iterate(self):
        while not self.isConverged and self.totalIterations < self.maxIterations:
            self.increaseShanksLevel()
            self.iterateBase()
            self.iterateShanks()
            self.iterateBase()
            self.iterateShanks()
            self.assessConvergence()
