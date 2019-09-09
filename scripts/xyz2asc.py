# Convert a .csv/.xyz bathymetry file to an ESRI ASCII regular grid (.asc)
# Last updated: April 19, 2019

import numpy as np
from scipy.interpolate import griddata

def xyz2asc(filename, separator, spacing, nodata_value):
    try:
        ascfile = filename + '.asc'
        np.set_printoptions(formatter={'float_kind':'{:f}'.format})
        # Read bathymetry file
        x,y,z = np.loadtxt(filename, delimiter='\t', usecols=(0,1,2), unpack=True)
        xmin = min(x)
        ymin = min(y)
        xmax = max(x)
        ymax = max(y)
        ncols = int((xmax - xmin)/spacing)
        nrows = int((ymax - ymin)/spacing)
        # Generate grid with data
        xi, yi = np.mgrid[xmin:xmax:ncols*1j, ymin:ymax:nrows*1j]
        # Interpolate bathymetry. Method can be 'linear', 'nearest' or 'cubic'
        zi = griddata((x,y), z, (xi, yi), method='linear')
        # Change Nans for values
        zi[np.isnan(zi)] = nodata_value
        # Flip array in the left/right direction
        zi = np.fliplr(zi)
        # Transpose it
        zi = zi.T
        # Write ESRI ASCII Grid file
        header = "NCOLS %d \nNROWS %d\nXLLCORNER %f\nYLLCORNER %f\nCELLSIZE %f\nNODATA_VALUE %s" % (int(ncols), int(nrows), float(xmin), float(ymin), spacing, nodata_value)
        np.savetxt(ascfile, zi, fmt='%f', header=header, comments='', delimiter=' ', newline='\n')
        print('File %s saved successfuly.' % ascfile)
    except:
        print('Something bad happened. File could not be generated.')

def main():
    # Convert xyz file with tab-separated columns, 0.001 degrees spacing and -9999 as nodata value
    xyz2asc('Port_Barcelona_25cm_2016.emo', '\t', 0.001, -9999)

if __name__ == '__main__':
    main()