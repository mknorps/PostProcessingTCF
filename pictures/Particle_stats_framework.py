# import of all the necessary packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import expanduser, exists
from pplib import tcf_parsers



# frequently changed constants
StList = ['1','5','25']

#file_path    = expanduser("~") + "/results_for_PhD/SGS_model_results/FRACTAL/"
file_path    = expanduser("~") + "/results_for_PhD/DNS/"
#file_path    = expanduser("~") + "/results_for_PhD/test/"
fig_path     = file_path

ModelLabel='model'
model_type='sgs' # sgs or tot - for fluid velocity at particle position


# declaration of constants

reference_path_LES  = expanduser("~") +"/REFERENCE_DATA/pure_LES/int2/"
reference_path_DNS  = expanduser("~") +"/REFERENCE_DATA/Marchiolli_DATA/TUE/"
#CommentRows = 58
CommentRows = 49
#CommentRows = 64
CommentRows_LES = 49
CommentRows_DNS = 47
tauplus = 0.0433 
pi = 3.1415

# declaration of picture attributes

StListLineStyle = ['k-^','-o','--','*']

# declaration of variables
model = {}
LES = {}
DNS = {}



#######################################
# data loading
#######################################

for i,x in enumerate(StList):
    model[x] = tcf_parsers.parse_particle_stats(file_path + 'particle_stat_' + x)
    LES[x] =  tcf_parsers.parse_particle_stats(reference_path_LES +'particle_stat_' + x)
    DNS[x] = tcf_parsers.parse_particle_stats(reference_path_DNS +'dns_particles_' + x)


#############################################
# Statistics
#  -  mean, rms and covariance on one picture
#############################################

columns = {} # list of columns for mean, correlation and three rms figures
columns['Us'] = {"LES":[24,32,28,29,30],
#                 "model":[24,32,28,29,30],
                 "model":[11,17,14,15,16],
                 "DNS":[11,17,14,15,16] }
columns['Vp'] = {"LES":[2,10,6,7,8],
#                 "model":[2,10,6,7,8],
                 "model":[2,8,5,6,7],
                 "DNS":[2,8,5,6,7] }
columns_concentration = {}
columns_concentration['Us'] = {"LES":[1,32,28,29,30],
                 "model":[1,32,28,29,30],
#                 "model":[1,17,14,15,16],
                 "DNS":[1,17,14,15,16] }
columns_concentration['Vp'] = {"LES":[1,10,6,7,8],
                 "model":[1,10,6,7,8],
#                 "model":[1,8,5,6,7],
                 "DNS":[1,8,5,6,7] }
line_style_dict = {"St1DNS": {"ls":"solid", "color":"blue", "label":"$St1$","lw":1.5},
                   "St1LES": {"ls":"dashed", "color":"blue","lw":1.5},
                   "St1model": {"ls":"dotted", "color":"blue","lw":2.5},
                   "St5DNS": {"ls":"solid", "color":"red", "label":"$St5$","lw":1.5},
                   "St5LES": {"ls":"dashed", "color":"red","lw":1.5},
                   "St5model": {"ls":"dotted", "color":"red","lw":2.5},
                   "St25DNS":{"ls":"solid", "color":"green", "label":"$St25$","lw":1.5},
                   "St25LES":{"ls":"dashed", "color":"green","lw":1.5},
                   "St25model":{"ls":"dotted", "color":"green","lw":2.5}
} 


def panel(pict_path,data):
    '''
    Draw statistics in form of
    a panel of figures.

    Input
    -----
    pict_path: path to save panel of figures
    data = {'ax0':p0,'ax1':p1,'ax2':p2,'ax3':p3,'ax4':p4}: 
            p0--p4 are dictionaries containing data 
            and parameters for plots that must contain:
            - 'xlim': [a,b]
            - 'ylim':[a,b]
            - 'xlabel': 'xlabel'
            - 'title' :"plot title"
            - 'ax' : list of dictionaries containing one curve data + plot parameters:
                'x' - x axis data
                'y' - y axis data
                'style' - dictionary of plot style

    Output
    ------
    none

    Result
    ------
    Panel of figures saved in pict_path.
    '''

    fig = plt.figure(figsize = (12,9))
    ax0 = plt.subplot2grid((7,2),(0,0),rowspan=4) #mean Ux
    ax1 = plt.subplot2grid((7,2),(4,0),rowspan=3) #<Ux,Uy>
    ax2 = plt.subplot2grid((7,2),(0,1),rowspan=3) #rms Ux
    ax3 = plt.subplot2grid((7,2),(3,1),rowspan=2) #rms Uy
    ax4 = plt.subplot2grid((7,2),(5,1),rowspan=2) #rms Uz
    ax_keys = ['ax0','ax1','ax2','ax3','ax4']
    ax_vals = [ax0,ax1,ax2,ax3,ax4]
    ax = dict(zip(ax_keys,ax_vals))


    for key,figure in ax.items():
        # setting up plot properties
        fig_keys = data[key].keys()
        figure.tick_params(axis='both',labelsize=15)
        if 'title' in fig_keys:
            figure.set_title(data[key]['title'])
        if 'xlim' in fig_keys:
            figure.set_xlim(data[key]['xlim'],
                            fontsize=15)
        if 'ylim' in fig_keys:
            figure.set_ylim(data[key]['ylim'])
        if 'xlabel' in fig_keys:
            figure.set_xlabel(data[key]['xlabel'],
                              fontsize=15)
        # plotting data
        if 'ax' in fig_keys:
            for ax_data in data[key]['ax']:
                figure.plot(ax_data['x'], ax_data['y'],
                             **ax_data['style'])

    leg = ax0.legend(fontsize=15)
    plt.tight_layout()
    fig.savefig(pict_path)
    plt.close(fig)


def ax_data_generator(column, *data):
    ''' 
    generate data for 'ax' value of panel

    Input
    -----
    column - name of column for wich the ax figure is drawn
    data_frames - list of data frames with defined plot styles,
                  example:
                  [{'data':df_LES, 'style':style_dict}]
    Output
    ------
    ax_data - list of dictionaries:
              {'x':x_data, 'y':y_data, 'style':style_dict}

    '''
    ax_data = []
    for d in data:
        new_line = {'x': d['data']['y+'],
                    'y': d['data'][column],
                    'style':d['style']}
        ax_data.append(new_line)

    return ax_data


def velocity_panel():
    for velocity,col in columns.items():

        fig = plt.figure(figsize = (12,9))
        ax0 = plt.subplot2grid((7,2),(0,0),rowspan=4) #mean Ux
        ax1 = plt.subplot2grid((7,2),(4,0),rowspan=3) #<Ux,Uy>
        ax2 = plt.subplot2grid((7,2),(0,1),rowspan=3) #rms Ux
        ax3 = plt.subplot2grid((7,2),(3,1),rowspan=2) #rms Uy
        ax4 = plt.subplot2grid((7,2),(5,1),rowspan=2) #rms Uz
        ax = [ax0,ax1,ax2,ax3,ax4]

        for figure in ax:
            figure.set_xlim([0,160])
            figure.tick_params(axis='both',labelsize=15)
        for figure in [ax3,ax4]:
            figure.set_ylim([0,1.2])
        for figure in [ax1,ax4]:
            figure.set_xlabel("$y^{+}$",fontsize=15)

        ax0.set_title('$\langle '+ velocity +'_x\\rangle^{+}$',fontsize=15)
        ax1.set_title('$\langle '+ velocity +'_x,' + velocity +'_y \\rangle^{+}$',fontsize=15)
        ax2.set_title('$rms('+ velocity +'_x)^{+}$',fontsize=15)
        ax3.set_title('$rms('+ velocity +'_y)^{+}$',fontsize=15)
        ax4.set_title('$rms('+ velocity +'_z)^{+}$',fontsize=15)

        for x in StList:
            for i,subplot in enumerate(ax):
                subplot.plot(data_LES[x][:,0],data_LES[x][:,col["LES"][i]], **line_style_dict["St"+x+"LES"])
                subplot.plot(data[x][:,0],data[x][:,col["model"][i]], **line_style_dict["St"+x+"model"])
                subplot.plot(data_DNS[x][:,0],data_DNS[x][:,col["DNS"][i]], **line_style_dict["St"+x+"DNS"])

        leg = ax0.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(fig_path + velocity + "_panel_fractal.pdf")
        plt.close(fig)


def ksgs_panel(pict_path,st,model,LES,DNS):

    for df in [model, DNS, LES]:
        df[st]['ksgs'] = 0.5*(df[st]['rms vx']**2 + df[st]['rms vy']**2
                             + df[st]['rms vz']**2)

    p = []
    for fig_name in ['ksgs',
        'average vx*vy','rms vx','rms vy', 'rms vz']:    
        p.append(ax_data_generator(fig_name,
            {'data':model[st],'style':{'label':'model'}},
            {'data':LES[st],'style':{'label':'LES'}},
            {'data':DNS[st],'style':{'label':'DNS'}}))

    data_with_parameters = {
        'ax0':{'title':'$k_{sg}^{+}$','ax':p[0]},
         'ax1':{'title':'$\langle V_x,V_y \\rangle^{+}$','ax':p[1]},
         'ax2':{'title':'$rms(V_x)^{+}$','ax':p[2]},
         'ax3':{'title':'$rms(V_y)^{+}$','ax':p[3]},
         'ax4':{'title':'$rms(V_z)^{+}$','ax':p[4]}
    }


    panel(pict_path,data_with_parameters)



def concentration_panel():
    for velocity,col in columns_concentration.items():

        fig = plt.figure(figsize = (12,9))
        ax0 = plt.subplot2grid((7,2),(0,0),rowspan=4) #mean Ux
        ax1 = plt.subplot2grid((7,2),(4,0),rowspan=3) #<Ux,Uy>
        ax2 = plt.subplot2grid((7,2),(0,1),rowspan=3) #rms Ux
        ax3 = plt.subplot2grid((7,2),(3,1),rowspan=2) #rms Uy
        ax4 = plt.subplot2grid((7,2),(5,1),rowspan=2) #rms Uz
        ax = [ax0,ax1,ax2,ax3,ax4]

        for figure in ax:
            figure.set_xlim([0.1,160])
            figure.tick_params(axis='both',labelsize=15)
        for figure in [ax3,ax4]:
            figure.set_ylim([0,1.2])
        for figure in [ax1,ax4]:
            figure.set_xlabel("$y^{+}$",fontsize=15)
        ax0.set_xscale('log')
        ax0.set_yscale('log')

        ax0.set_title('$m_{1}$',fontsize=15)
        ax1.set_title('$\langle '+ velocity +'_x,' + velocity +'_y \\rangle^{+}$',fontsize=15)
        ax2.set_title('$rms('+ velocity +'_x)^{+}$',fontsize=15)
        ax3.set_title('$rms('+ velocity +'_y)^{+}$',fontsize=15)
        ax4.set_title('$rms('+ velocity +'_z)^{+}$',fontsize=15)

        for n,x in enumerate(StList):
            for i,subplot in enumerate(ax):
                subplot.plot(data['LES'][x][:,0],data['LES'][x][:,col["LES"][i]], **line_style_dict["St"+x+"LES"])
                subplot.plot(data['model'][x][:,0],data['model'][x][:,col["LES"][i]], **line_style_dict["St"+x+"model"])
                #subplot.plot(data[n][:,0],data[n][:,col["model"][i]],label=str(n+1))
                #subplot.plot(data["0.2"][:,0],data["0.2"][:,col["model"][i]],label="St0.2 -model")
                subplot.plot(data['DNS'][x][:,0],data['DNS'][x][:,col["DNS"][i]], **line_style_dict["St"+x+"DNS"])

        leg = ax0.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(fig_path + velocity + "_concentration_panel3.pdf")
        plt.close(fig)

if __name__=='__main__':

    #velocity_panel()
    #ksgs_panel()
    pwd_stat = '/home/gemusia/results_for_PhD/DNS/particle_stat_1'
    df = tcf_parsers.parse_particle_stats(pwd_stat)

    for x in StList:
        ksgs_panel("test_panel_{}.pdf".format(x),x,model,LES,DNS)
