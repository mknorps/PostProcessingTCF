# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: DNSvsFiltered_heatmap.py
# Created by: gemusia
# Creation date: 18-01-2018
# Last modified: 18-01-2018 11:55:02
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
import matplotlib.pyplot as plt
from os.path import expanduser
import pandas as pd

#parameters
dns_fields=["upp_Ux","upp_Uy","upp_Uz"]
apriori_fields=["uppf_Ux","uppf_Uy","uppf_Uz"]
dns_dimensions = (128,129,128)
apriori_dimensions = (32,33,64)
dns_shift = (129,128,128)
apriori_shift = (33,64,32)


file_path    = expanduser("~") + "/wyniki/apriori/fluid/"
fig_path     = file_path

def load_data(field=2501):

    dns_files = [file_path+x+'_'+str(field) for x in dns_fields]
    apriori_files = [file_path+x+'_'+str(field) for x in apriori_fields]


    data = {}

    for field, field_file in zip(dns_fields,dns_files):
        with open(field_file, 'r') as f:
            data_load = np.loadtxt(f)        
            data_reshaped = data_load.reshape(*dns_shift)
            # original input has permuted directions 
            # (left - input, right - standard naming convention, applied here)
            # (Ux,Uy,Uz) --> (Uy,Uz,Ux)
            data_transposed = np.transpose(data_reshaped, axes=(2,0,1))
            data[field] = np.array(data_transposed)

    for field, field_file in zip(apriori_fields,apriori_files):
        with open(field_file, 'r') as f:
            data_load = np.loadtxt(f)        
            data_reshaped = data_load.reshape(*apriori_shift)
            # original input has permuted directions 
            # (left - input, right - standard naming convention, applied here)
            # (Ux,Uy,Uz) --> (Uy,Uz,Ux)
            data_transposed = np.transpose(data_reshaped, axes=(2,0,1))
            data[field] =np.array( data_transposed)
    return data 

def cut_slice(data,y=0):

    slices = {}
    for field in dns_fields:
        slices[field] =data[field][:,dns_dimensions[1]//2,:]  

    for field in apriori_fields:
        slices[field] =data[field][:,apriori_dimensions[1]//2,:]  

    return slices


def draw_heatmaps(slices,pict_path):

    fig = plt.figure(figsize = (12,4))
    ax1 = plt.subplot2grid((1,2),(0,0)) #tme_xx
    ax2 = plt.subplot2grid((1,2),(0,1)) #time_yy
    ax = [ax1,ax2]

    for figure in ax:
        figure.xaxis.set_ticklabels([])
        figure.yaxis.set_ticklabels([])
        figure.xaxis.set_visible(False)
        figure.yaxis.set_visible(False)

        figure.set_xlabel("$x$",fontsize=15)
        figure.set_ylabel("$z$",fontsize=15)
        #figure.set_xlim([0,2*np.pi])
        #figure.set_ylim([0,np.pi])

    #ax1.set_title("DNS" ,fontsize=15)
    #ax2.set_title("a priori" ,fontsize=15)

    ax1.imshow(slices['upp_Ux'], aspect='auto',cmap='ocean', interpolation='nearest')
    ax2.imshow(slices['uppf_Ux'],aspect='auto', cmap='ocean', interpolation='nearest')

    #leg = ax3.legend(fontsize=15)
    plt.tight_layout(pad=0, w_pad=0,h_pad=0)#
    fig.savefig(pict_path )
    plt.close(fig)
    


if __name__=='__main__':
    
    data = load_data()
    slices = cut_slice(data)

    pic_path = fig_path + "heatmaps.png"
    draw_heatmaps(slices,pic_path)
