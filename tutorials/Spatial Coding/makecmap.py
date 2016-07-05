from pylab import *
import matplotlib.cm as cmx
import matplotlib.colors as colors

def MakeColourMap(N, colormap='jet'):

	'''
	To make colour map with N possible colours. Interpolated from map 'colormap'
	'''
	### Colour map for cells (if you want to plot multiple cells)
	values = range(N)
	jet = cm = plt.get_cmap(colormap)
	cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
	scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

	return scalarMap