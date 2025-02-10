import matplotlib.colors as col

def getColorMap(right = '#C96868', up = '#FADFA1', left = '#FFF4EA', down = '#7EACB5'):
    colors = [left,down,right,up,left]
    return col.LinearSegmentedColormap.from_list('myMap',colors,N=256,gamma=1.0)
