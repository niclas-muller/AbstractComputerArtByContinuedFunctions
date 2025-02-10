import cProfile
import numpy as np
from main import ContinuedFunctionArtFrame

center = (-1,2)
extent = 1
resolution = 100
a = 0.6889056865544987-0.000507424433446868j 
b = 0.027905233067976765-0.5703520544167373j
func = f'sin_sin_mul:{a}_add:{b}_log'

with cProfile.Profile() as pr:
    frame = ContinuedFunctionArtFrame(func, center, extent, resolution)
    pr.print_stats(sort='cumtime')
