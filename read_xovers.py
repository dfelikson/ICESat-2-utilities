# -*- coding: utf-8 -*-
"""
Created on Thu May  2 09:56:05 2019

@author: ben smith

Edited by Denis Felikson Dec 2021
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import pointCollection as pc
import glob
import re
import h5py

def read_xovers(xover_dir, verbose=False, wildcard='*', r_limits=[0, 1.e7], delta_t_min=0, delta_t_max=2592000):
    """
    read_xovers: Read all the crossover files in a directory (or matching a glob)

    Inputs:
        xover_dir: directory to search
        verbose: set to 'true' to see errors reading crossover files (default is silent)
        wildcard: default is '*'.  Specify to match selected files
        r_limits: limits for the polar stereographic coordinates of the tile files.  
            Default of [0, 1e7] eliminates crossovers with lat=0 (a common error in early versions)  
        delta_t_min: minimum crossover time difference, in seconds.  Default is 0
        delta_t_max: maximum crossover time difference, in seconds.  Default of 2592000 is 1 month

    Outputs:
        v: dict of nx2 matrices, giving ATL06 parameters interpolated to the crossover locations.  The first
            column gives the value for the first measurement in the crossover, the second the value from the second.
        delta: dict of nx1 matrices, giving ATL06 parameter differences between the crossover measurents, late minus early
        bar: dict of nx1 matrices, giving ATL06 parameter averages between the crossover measurents
        meta: metadata values at the crossovers
    """


    tiles=glob.glob(xover_dir+'/*.h5')
    if verbose: print('Found {:d} crossover tiles'.format(len(tiles)))
    with h5py.File(tiles[0],'r') as h5f:
        fields=[key for key in h5f['data_0'].keys()]
    
    D=[]
    meta=[]

    tile_re=re.compile('E(.*)_N(.*).h5')
    tiles=glob.glob(xover_dir+'/'+wildcard+'.h5')
    if verbose: print('Reading {:d} crossover tiles'.format(len(tiles)))
    for tile in tiles:
        m=tile_re.search(tile)
        if m is not None:
            r2=np.float(m.group(1))**2+np.float(m.group(2))**2
            if (r2 < r_limits[0]**2) or (r2 > r_limits[1]**2):
                continue
        try:
            this_D=[pc.data().from_h5(tile, field_dict={gr : fields}) for gr in ['data_0','data_1']]
            this_meta=pc.data().from_h5(tile, field_dict={None:['slope_x', 'slope_y','grounded']})
            good = np.logical_and( np.abs(this_D[1].delta_time[:,0]-this_D[0].delta_time[:,0]) < delta_t_max, \
                                   np.abs(this_D[1].delta_time[:,0]-this_D[0].delta_time[:,0]) > delta_t_min)
            for Di in this_D:
                Di.index(good)
            this_meta.index(good)

        except KeyError:
            if verbose:
                print("failed to read " + tile)
            continue

        D.append(this_D)
        meta.append(this_meta)

    meta=pc.data().from_list(meta)
    v={}
    for field in fields:
        vi=[]
        for Di in D:
            vi.append(np.r_[[np.sum(getattr(Di[ii], field)*Di[ii].W, axis=1) for ii in [0, 1]]])
        v[field]=np.concatenate(vi, axis=1).T
    delta={field:np.diff(v[field], axis=1) for field in fields}
    bar={field:np.mean(v[field], axis=1) for field in fields}
    
    if verbose: print('Tiles contain {:d} crossovers'.format(len(bar['BP'])))

    return v,  delta,  bar, {key:getattr(meta, key) for key in meta.fields}
