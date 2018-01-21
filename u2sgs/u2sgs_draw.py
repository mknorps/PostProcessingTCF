# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs_stats.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 20-01-2018 10:25:47
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from itertools import product

from pplib import parameters as p
import input_files as f

def unify_columns(data):

    for panel in ['apriori','LES']:
        for d in p.DirectionList:
            data[panel]['usgs_'+d+'_rms'] = np.sqrt(data[panel]['u2sgs_'+d])
        data[panel]['usgs_x_usgs_y'] = data[panel]['u2sgs_xy']
        
    return data


class DrawU2sgs(pd.Panel):


    def __init__(self):

        data =  pd.read_excel(f.file_path_write, sheet_name = None)
        unified_data = unify_columns(data)

        super().__init__(unified_data)


    def symmetrise(self):

        symm_columns =list(set(self['def'].columns) - set(f.asymm_columns)) 
        data_symm = self
        for s,c in product(f.types,symm_columns):
            lst = data_symm[s][c]
            l = len(lst)
            data_symm[s][c] = 0.5*(lst[:(l+1)//2-1] + np.flipud(lst)[1:(l+1)//2])
        for s,c in product(f.types,f.asymm_columns):
            lst = data_symm[s][c]
            l = len(lst)
            data_symm[s][c] = 0.5*(lst[:(l+1)//2-1] - np.flipud(lst)[1:(l+1)//2])

        for s in ['apriori','LES']:
            data_symm[s]['y'] = (1-data_symm[s]['y'])*p.Retau
        data_symm['def']['y'] = (1+data_symm['def']['y'])*p.Retau


        data_return = data_symm
        
        return data_return

    def draw_u2sgs(self,pict_path,is_symm=True):

        fig = plt.figure(figsize = (12,6))
        ax1 = plt.subplot2grid((1,3),(0,0)) #tme_xx
        ax2 = plt.subplot2grid((1,3),(0,1)) #time_yy
        ax3 = plt.subplot2grid((1,3),(0,2)) #time_zz
        ax = [ax1,ax2,ax3]

        if is_symm:
            data = self.symmetrise()
            for figure in ax:
                figure.set_xlim([0,150])
                figure.set_ylim([0,1.7])
                figure.tick_params(axis='both',labelsize=15)
                figure.set_xlabel("$y^{+}$",fontsize=15)
        else:
            data = self
            for figure in ax:
                figure.set_xlim([-1,1])
                figure.tick_params(axis='both',labelsize=15)
                figure.set_xlabel("$y$",fontsize=15)

        ax1.set_title("$\sigma(u_{x})^{+}$" ,fontsize=15)
        ax2.set_title("$\sigma(u_{y})^{+}$" ,fontsize=15)
        ax3.set_title("$\sigma(u_{z})^{+}$" ,fontsize=15)

        for i,subplot in zip(p.DirectionList,ax):
            for simulation in f.types:
                subplot.plot(data[simulation]['y'],data[simulation]["usgs_"+i+"_rms"],label=simulation,lw=3)

        leg = ax3.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)

    def draw_cov_xy(self,pict_path,is_symm=True):

        data = self
        fig = plt.figure(figsize = (6,6))
        ax1 = plt.subplot2grid((1,2),(0,0)) #time_zz
        ax2 = plt.subplot2grid((1,2),(0,1)) #time_zz
        ax = [ax1,ax2]

        if is_symm:
            #data = self.symmetrise()
            for figure in ax:
                figure.set_xlim([0,150])
                figure.tick_params(axis='both',labelsize=15)
                figure.set_xlabel("$y^{+}$",fontsize=15)
        else:
            for figure in ax:
                figure.set_xlim([-1,1])
                figure.tick_params(axis='both',labelsize=15)
                figure.set_xlabel("$y$",fontsize=15)

        ax1.set_title("$Cov(u_{x},u_y)^{+}$" ,fontsize=15)
        ax2.set_title("$\\rho(u_{x},u_y)$" ,fontsize=15)

        for simulation in ['apriori','LES']:
            ax1.plot(data[simulation]['y'],data[simulation]["usgs_x_usgs_y"],label=simulation)
            correlation = np.divide(data[simulation]["usgs_x_usgs_y"], data[simulation]["usgs_x"]*data[simulation]["usgs_y"])
            ax2.plot(data[simulation]['y'],correlation,label=simulation)
        ax1.plot(data['def']['y'],data['def']["cov_xy"],label='def')
        correlation = np.divide(data['def']["usgs_x_usgs_y"], data['def']["usgs_x"]*data['def']["usgs_y"])
        ax2.plot(data['def']['y'],correlation,label='def')

        leg = ax2.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)

    def draw_ksgs(self,pict_path,is_symm=True):

        data = self
        fig = plt.figure(figsize = (6,4))
        ax = plt.subplot2grid((1,1),(0,0)) 

        if is_symm:
            ax.set_xlim([0.3,150])
            ax.set_xscale('log')
            ax.tick_params(axis='both',labelsize=15)
            ax.set_xlabel("$y^{+}$",fontsize=15)
        else:
            ax.set_xlim([-1,1])
            ax.tick_params(axis='both',labelsize=15)
            ax.set_xlabel("$y$",fontsize=15)

        ax.set_title("$k_{sg}^{+}$" ,fontsize=15)

        for simulation in f.types:

            ksgs = 0.5 * (data[simulation]["usgs_x_rms"]**2 +\
                   data[simulation]["usgs_y_rms"]**2 +\
                   data[simulation]["usgs_z_rms"]**2)
            ax.plot(data[simulation]['y'],ksgs,label=simulation,lw=3)

        leg = ax.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)

    def draw_sigma_check(self,pict_path,is_symm=True):

        tau_data = pd.read_csv("~/wyniki/time_scales_ii/tau.csv")
        tau = (tau_data['fluid_SGSles_x']+tau_data['fluid_SGSles_y']+tau_data['fluid_SGSles_z'])/3.0 
        tau_long = [tau[0]/2,tau[0]]
        for t1,t2 in zip(tau[1:],tau[:-1]):
            tau_long.append(t1)
            tau_long.append((t1+t2)/2)
        tau_long.append(t1)    
        tau_long = np.array(tau_long)
        print(tau)
        print(tau_long)

        graduf = np.array([ 0.62424453, 1.05721209, 0.8779482,  0.7037418, 0.50064856, 0.31515047, 0.18369803, 0.10714933, 0.06798791, 0.04899518, 0.03922657, 0.0364343, 0.03330875,0.02768044,0.02199585,0.0119288, 0.])

        l = len(graduf)
        data = self
        fig = plt.figure(figsize = (6,4))
        ax = plt.subplot2grid((1,1),(0,0)) 

        if is_symm:
            #ax.set_xlim([0.3,150])
            #ax.set_xscale('log')
            ax.tick_params(axis='both',labelsize=15)
            ax.set_xlabel("$y^{+}$",fontsize=15)
        else:
            ax.set_xlim([-1,1])
            ax.tick_params(axis='both',labelsize=15)
            ax.set_xlabel("$y$",fontsize=15)

        ax.set_title("$k_{sg}^{+}$" ,fontsize=15)

        for simulation in f.types:
            check = data[simulation]["usgs_x_rms"][:l]**2 -\
                   data[simulation]["usgs_x_usgs_y"][:l]**2/\
                   data[simulation]["usgs_y_rms"][:l]**2- \
                   data[simulation]["usgs_y_rms"][:l]**2 *\
                   tau_long**2/4* graduf
            print( check)

            ax.plot(data[simulation]['y'][:l],check,label=simulation,lw=3)

        leg = ax.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)
