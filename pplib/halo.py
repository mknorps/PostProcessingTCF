# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: halo.py
# Created by: gemusia
# Creation date: 27-02-2018
# Last modified: 27-02-2018 20:55:03
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pandas as pd

def points_with_halo(points,col1,col2, offset_pcnt):
    '''
    adds a halo to dataframe 'points' 
    for columns 'col1' and 'col2'

    '''

    xmin = min(points[col1])
    xmax = max(points[col1])
    ymin = min(points[col2])
    ymax = max(points[col2])

    #vertical halo
    halo_offset = offset_pcnt*(xmax-xmin)
    top_halo = points[points[col1] < xmin+halo_offset].copy()
    bottom_halo = points[points[col1] > xmax-halo_offset].copy()

    top_halo.loc[:,col1] = top_halo[col1] + (xmax-xmin)
    bottom_halo.loc[:,col1] = bottom_halo[col1] - (xmax-xmin)

    vertical_halo = pd.concat([points,top_halo,bottom_halo],ignore_index=True)

    #horisontal halo
    halo_offset = offset_pcnt*(ymax-ymin)
    right_halo = vertical_halo[vertical_halo[col2] < ymin + halo_offset].copy()
    left_halo = vertical_halo[vertical_halo[col2] > ymax - halo_offset].copy()

    right_halo.loc[:,col2] = right_halo[col2] + (ymax-ymin)
    bottom_halo.loc[:,col2] = bottom_halo[col2] - (ymax-ymin)

    df = pd.concat([vertical_halo,right_halo,left_halo],ignore_index=True)

    df.drop_duplicates(inplace=True)

    return df

