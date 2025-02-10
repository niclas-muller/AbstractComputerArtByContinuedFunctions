import numpy as np

class FuncGen():

    def __init__(self,seq):
        """
            This class creates a function from an ordered sequence of function types. 
            Available functions are:
                - mul: multiplication by constant (needs to be passed)
                - add: addition with constant (needs to be passed)
                - pow: raise to power (needs to be passed)
                - log: compute natural log
                - sin: compute sin

            Example: in order to encode the function sin(log(c0 + c1*sqrt(z))) we write:
            seq = 'pow:0.5_mul:c1_add:c0_log_sin', so functional elements are separated by
            underscores, parameterized functions are appended by the respective parameter 
            after a colon.
        """
        self.seq = seq
        self.constructFunc()

    def constructFunc(self):

        def createFuncAtom(funcElem):
            funcElem = funcElem.split(':')
            if len(funcElem) == 2:
                param = np.complex128(funcElem[1])
            match funcElem[0]:
                case 'mul':
                    return (lambda x: x*param)
                case 'add':
                    return (lambda x: x + param)
                case 'pow':
                    return (lambda x: x**param)
                case 'log':
                    return (lambda x: np.log(x))
                case 'sin':
                    return (lambda x: np.sin(x))
                case _:
                    raise NameError(f'Undefined function atom {funcElem}')

        funcPlan = []
        for funcElem in self.seq.split('_'):
            funcPlan.append(createFuncAtom(funcElem))

        def chainedFunc(t):
            t += 0.j
            for f in funcPlan:
                t = f(t)
            return t

        self.func = chainedFunc
