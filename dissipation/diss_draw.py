# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs_stats.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 11-01-2018 10:23:29
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


labels = {'apriori_tot':{'label':'$\epsilon_{DNS}$','lw':2,'color':'blue'}, 
	  'apriori_LES':{'label':'$\epsilon_{apriori}$','lw':2,'color':'red'},
	  'apriori_SGS':{'label':'$\epsilon_{SGS}$','lw':2,'color':'black'},
	  'apriori_model1':{'label':'$\epsilon_{1}^{apriori}$','lw':2,'color':'red'},
	  'LES_model1':{'label':'$\epsilon_{1}^{LES}$','lw':2,'color':'red','linestyle':'dashed'},
	  'apriori_model2':{'label':'$\epsilon_{2}^{apriori}$','lw':2,'color':'blue'},
	  'LES_model2':{'label':'$\epsilon_{2}^{LES}$','lw':2,'color':'blue','linestyle':'dashed'},
	  'LES':{'label':'$\epsilon_{LES}$','lw':2,'color':'green'}} 

def draw_diss_tot(file_path,pict_path,is_symm=True):

    fig = plt.figure(figsize = (6,4))
    ax1 = plt.subplot2grid((1,1),(0,0))

    data =  pd.read_excel(file_path, sheet_name = None)

    if is_symm:
        ax1.set_xlim([0.3,150])
        ax1.set_xscale('log')
        ax1.set_xlabel("$y^{+}$",fontsize=15)
        ax1.set_ylabel("$\epsilon^{+}$",fontsize=15)
    ax1.tick_params(axis='both',labelsize=15)


    ax1.plot(data['apriori']['y'],data['apriori']['epsl_tot'],**labels['apriori_tot'])
    ax1.plot(data['apriori']['y'],data['apriori']['epsl_LES'],**labels['apriori_LES'])
    ax1.plot(data['LES']['y'],data['LES']['epsl_tot'],**labels['LES'])

    leg = ax1.legend(fontsize=15)
    plt.tight_layout()
    fig.savefig(pict_path )
    plt.close(fig)

def draw_diss_model(file_path,pict_path,is_symm=True):

    fig = plt.figure(figsize = (6,4))
    ax1 = plt.subplot2grid((1,1),(0,0))

    data =  pd.read_excel(file_path, sheet_name = None)

    if is_symm:
        ax1.set_xlim([0.04,160])
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel("$y^{+}$",fontsize=15)
        ax1.set_ylabel("$\epsilon^{+}$",fontsize=15)
    ax1.tick_params(axis='both',labelsize=15)


    ax1.plot(data['apriori']['y'],data['apriori']['epsl_tot']-data['apriori']['epsl_LES'],**labels['apriori_SGS'])
    ax1.plot(data['apriori']['y'],data['apriori']['epsl_model2'],**labels['apriori_model2'])
    ax1.plot(data['LES']['y'],data['LES']['epsl_model2'],**labels['LES_model2'])
    ax1.plot(data['apriori']['y'],data['apriori']['epsl_model1'],**labels['apriori_model1'])
    ax1.plot(data['LES']['y'],data['LES']['epsl_model1'],**labels['LES_model1'])

    leg = ax1.legend(fontsize=15)
    plt.tight_layout()
    fig.savefig(pict_path )
    plt.close(fig)

