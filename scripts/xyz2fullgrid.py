# Convert a .csv/.xyz bathymetry file to another .csv/.xyz file with a full grid with zero-value points
# Last updated: May 23, 2019
#sort -k2 -n -k1 353_Girona_fullgrid.xyz -o 353_Girona_fullgrid_sort.xyz
#gdal_translate -of NetCDF 353_Girona_fullgrid_sort.xyz 353_Girona_fullgrid.nc

from pylab import *
import numpy as np

def xyz2fullgrid(filename, extension, separator):
    try:
        x,y,z = np.loadtxt(filename + extension, delimiter=separator, usecols=(0,1,2), unpack=True)
        xmin = min(x)
        xmax = max(x)

        ymin = min(y)
        ymax = max(y)

        mdx = abs(diff(x))
        mdy = abs(diff(y))

        dx = median(mdx[where(mdx>0.0)[0]])
        dy = median(mdy[where(mdy>0.0)[0]])

        xi = arange(xmin,xmax+dx,dx)
        yi = arange(ymin,ymax+dy,dy)
        zi = ones((len(yi),len(xi)))*0

        ix = np.round((x-xmin)/dx).astype(int)
        iy = np.round((y-ymin)/dy).astype(int)
        zi[iy,ix] = z

        i = 0
        j = 0
        with open(filename + '.full.'+ extension, 'w') as fitxer:
            while i < len(xi):
                j = 0
                while j < len(yi):
                    fitxer.write('%f %f %f\n' % (xi[i], yi[j], zi[j,i]))
                    j += 1
                i += 1
        print('File %s saved successfuly.' % (filename + '_fullgrid'+ extension))
    except:
        print('Something bad happened. File could not be generated.')

def main():
    xyz2fullgrid('353_Girona', '.xyz', '\t')

if __name__ == '__main__':
    main()