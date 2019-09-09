# Calculate regular grid by extent and spacing
# Last updated: April 18, 2019

import pyproj
import shapely.geometry

def generateRegularGrid(x_lo, x_hi, y_lo, y_hi, gridSpacingMeters):
    print('Computing grid...')
    p_ll = pyproj.Proj(init='epsg:4326') # lon, lat
    p_mt = pyproj.Proj(init='epsg:3857') # metric
    sw = shapely.geometry.Point((x_lo, y_lo))
    ne = shapely.geometry.Point((x_hi, y_hi))
    s = pyproj.transform(p_ll, p_mt, sw.x, sw.y) # transform South West point to 3857
    e = pyproj.transform(p_ll, p_mt, ne.x, ne.y) # .. same for North East
    gridpoints = []
    x = s[0]
    while x < e[0]:
        y = s[1]
        while y < e[1]:
            p = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x, y))
            gridpoints.append(p)
            y += gridSpacingMeters
        x += gridSpacingMeters
    lons = []
    lats = []
    for point in gridpoints:
        if point.x not in lons:
            lons.append(point.x)
        if point.y not in lats:
            lats.append(point.y)
    print('xpc: %f ypc: %f xlenc: %f ylenc: %f mxc: %s myc: %s' % (x_lo, y_lo, x_hi-x_lo, y_hi-y_lo, len(lons)-1, len(lats)-1))

def main():
    # Generate example grid with cell size of 500 meters
    generateRegularGrid(3.083, 3.166, 41.8125, 41.865, 50)

if __name__ == '__main__':
    main()