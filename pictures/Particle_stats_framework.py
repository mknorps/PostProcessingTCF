# import of all the necessary packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import expanduser, exists
from pplib import tcf_parsers

# declaration of constants
StList = ['1','5','25']
reference_path_LES  = expanduser("~") +"/REFERENCE_DATA/pure_LES/int2/"
reference_path_DNS  = expanduser("~") +"/REFERENCE_DATA/Marchiolli_DATA/TUE/"



#############################################
# Statistics
#  -  mean, rms and covariance on one picture
#############################################

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
        if 'xscale' in fig_keys:
            figure.set_xscale(data[key]['xscale'])
        if 'yscale' in fig_keys:
            figure.set_yscale(data[key]['yscale'])
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



def concentration_panel(pict_path,st,model,LES,DNS):
    p = []
    for fig_name in ['particle concentration',
        'average vx*vy','rms vx','rms vy', 'rms vz']:    
        p.append(ax_data_generator(fig_name,
            {'data':model[st],'style':{'label':'model'}},
            {'data':LES[st],'style':{'label':'LES'}},
            {'data':DNS[st],'style':{'label':'DNS'}}))

    data_with_parameters = {
            'ax0':{'title':'$C$','xscale':'log',
                   'yscale':'log',
                   'ax':p[0]},
         'ax1':{'title':'$\langle V_x,V_y \\rangle^{+}$','ax':p[1]},
         'ax2':{'title':'$rms(V_x)^{+}$','ax':p[2]},
         'ax3':{'title':'$rms(V_y)^{+}$','ax':p[3]},
         'ax4':{'title':'$rms(V_z)^{+}$','ax':p[4]}
    }


    panel(pict_path,data_with_parameters)

if __name__=='__main__':

    #######################################
    # data loading
    #######################################

    file_path    = expanduser("~") + "/results_for_PhD/DNS/"
    fig_path     = file_path

    model = {}
    LES = {}
    DNS = {}

    for i,x in enumerate(StList):
        model[x] = tcf_parsers.parse_particle_stats(file_path 
                + 'particle_stat_' + x)
        LES[x] =  tcf_parsers.parse_particle_stats(reference_path_LES 
                + 'particle_stat_' + x)
        DNS[x] = tcf_parsers.parse_particle_stats(reference_path_DNS 
                + 'dns_particles_' + x)


    #velocity_panel()
    #ksgs_panel()
    file_name = 'particle_stat_1'
    df = tcf_parsers.parse_particle_stats(file_path + file_name)

    for x in StList:
        concentration_panel(file_path + "concentration_panel_{}.pdf".format(x),x,model,LES,DNS)
