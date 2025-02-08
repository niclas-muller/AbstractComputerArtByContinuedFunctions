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
                - exp: compute exponential

            Example: in order to encode the function sin(log(c0 + c1*sqrt(z))) we write:
            seq = 'pow:0.5_mul:c1_add:c0_log_sin', so functional elements are separated by
            underscores, parameterized functions are appended by the respective parameter 
            after a colon.
        """
        self.seq = seq
        self.constructFunc()

    def constructFunc(self):
        funcPlan = []
        for _funcElem in self.seq.split('_'):
            funcElem = _funcElem.split(':')
            if len(funcElem) == 2:
                param = np.complex128(funcElem[1])
            match funcElem[0]:
                case 'mul':
                    funcPlan.append(lambda x: x*param)
                case 'add':
                    funcPlan.append(lambda x: x + param)
                case 'pow':
                    funcPlan.append(lambda x: x**param)
                case 'log':
                    funcPlan.append(lambda x: np.log(x))
                case 'sin':
                    funcPlan.append(lambda x: np.sin(x))
                case 'exp':
                    funcPlan.append(lambda x: np.exp(x))
                case _:
                    raise NameError(f'Undefined function atom {funcElem}')

        def chainedFunc(x):
            for funcAtom in funcPlan:
                x = funcAtom(x)
            return x

        self.func = chainedFunc
