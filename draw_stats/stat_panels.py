# import of all the necessary packages

import matplotlib.pyplot as plt
from os.path import expanduser

# declaration of constants
STLIST = ['1', '5', '25']
REFERENCE_PATH_LES = expanduser("~") + "/REFERENCE_DATA/pure_LES/int2/"
REFERENCE_PATH_DNS = expanduser("~") + "/REFERENCE_DATA/Marchiolli_DATA/TUE/"



#############################################
# Statistics
#  -  mean, rms and covariance on one picture
#############################################



def panel(pict_path, data):
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

    fig = plt.figure(figsize=(12, 9))
    ax0 = plt.subplot2grid((7, 2), (0, 0), rowspan=4) #mean Ux
    ax1 = plt.subplot2grid((7, 2), (4, 0), rowspan=3) #<Ux,Uy>
    ax2 = plt.subplot2grid((7, 2), (0, 1), rowspan=3) #rms Ux
    ax3 = plt.subplot2grid((7, 2), (3, 1), rowspan=2) #rms Uy
    ax4 = plt.subplot2grid((7, 2), (5, 1), rowspan=2) #rms Uz
    ax_keys = ['ax0', 'ax1', 'ax2', 'ax3', 'ax4']
    ax_vals = [ax0, ax1, ax2, ax3, ax4]
    ax = dict(zip(ax_keys, ax_vals))


    for key, figure in ax.items():
        # setting up plot properties
        fig_keys = data[key].keys()
        figure.tick_params(axis='both', labelsize=15)
        if 'title' in fig_keys:
            figure.set_title(data[key]['title'])
        if 'xlim' in fig_keys:
            figure.set_xlim(data[key]['xlim'])
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
                figure.plot(ax_data['x'], ax_data['y'], **ax_data['style'])

    ax0.legend(fontsize=15)
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




def ksgs_panel(pict_path, st, LES, DNS, velocity='u', **models):
    '''
    Draw a panel with SGS kinetic energy (ksgs)
    in the first subfigure

    Input
    -----
    pict_path - path to save panel of figures
    st        -  Stokes number of particles
                the key for LES, DNS and models dataframes
    LES - Pandas Panel object (or dict) containing DataFrames
          of Large Eddy Simulation reference data,
          keys are particle Stoke number
    DNS - Pandas Panel object (or dict) containing DataFrames
          of Direct Numerical Simulations reference data,
          keys are particle Stoke number
    velocity - 'u' (fluid) or 'v' (particle)
    models - {model_name: model_panel, ...}
             where model_panel is dict of DataFrames containing
             model statistics

    Output
    ------
    none

    Result
    ------
    Panel of figures saved in pict_path.

    '''

    for df in [DNS, LES]:
        df[st]['ksgs'] = 0.5*(df[st]['rms {}x'.format(velocity)]**2
              + df[st]['rms {}y'.format(velocity)]**2
              + df[st]['rms {}z'.format(velocity)]**2)

    models_local = []
    for key, val in models.items():
        val['ksgs'] = 0.5*(val['rms {}x'.format(velocity)]**2 
                + val['rms {}y'.format(velocity)]**2
                + val['rms {}z'.format(velocity)]**2)
        models_local.append(
            {'data':val,'style':{'label':key}})

    p = []
    for fig_name in ['ksgs',
            'average {}x'.format(velocity),'average {}y'.format(velocity),
            'average {}z'.format(velocity), 'particle concentration']:    
        p.append(ax_data_generator(fig_name,
            {'data':LES[st],'style':{'label':'LES', 'ls':'dashed','c':'red'}},
            {'data':DNS[st],'style':{'label':'DNS','ls':'solid','c':'red'}},
            *models_local))

    data_with_parameters = {
         'ax0':{'title':'$k_{sg}^{+}$', 'ax':p[0]},
         'ax1':{'title':'$\\langle {}_x \\rangle^{}$'.format(velocity,"+"), 'ax':p[1]},
         'ax2':{'title':'$\\langle {}_y \\rangle^{}$'.format(velocity,"+"), 'ax':p[2]},
         'ax3':{'title':'$\\langle {}_z \\rangle^{}$'.format(velocity,"+"), 'ax':p[3]},
         'ax4':{'title':'$C$','xscale':'log',
                   'yscale':'log',
                   'xlim':[0.1,160],
                   'ax':p[4]}
    }


    panel(pict_path,data_with_parameters)



def concentration_panel(pict_path, st, LES, DNS, velocity='u', **models):
    '''
    Draw a panel with SGS kinetic energy (ksgs)
    in the first subfigure

    Input
    -----
    pict_path - path to save panel of figures
    st        -  Stokes number of particles
                the key for LES, DNS and models dataframes
    LES - Pandas Panel object (or dict) containing DataFrames
          of Large Eddy Simulation reference data,
          keys are particle Stoke number
    DNS - Pandas Panel object (or dict) containing DataFrames
          of Direct Numerical Simulations reference data,
          keys are particle Stoke number
    velocity - 'u' (fluid) or 'v' (particle)
    models - {model_name: model_panel, ...}
             where model_panel is dict of DataFrames containing
             model statistics

    Output
    ------
    none

    Result
    ------
    Panel of figures saved in pict_path.
    '''
 
    models_local = []
    for key, val in models.items():
        models_local.append(
            {'data':val, 'style':{'label':key}})

    p = []
    for fig_name in ['particle concentration',
        'average {}x*{}y'.format(velocity,velocity),
        'rms {}x'.format(velocity), 'rms {}y'.format(velocity),  
        'rms {}z'.format(velocity)]:    
        p.append(ax_data_generator(fig_name,
            {'data':LES[st], 'style':{'label':'LES', 'ls':'dashed', 'c':'red'}}, 
            {'data':DNS[st], 'style':{'label':'DNS', 'ls':'solid', 'c':'red'}}, 
            *models_local))

    data_with_parameters = {
            'ax0':{'title':'$C$', 'xscale':'log', 
                   'xlim':[0.1,160],
                   'ax':p[0]},
         'ax1':{'title':'$\langle {}_x,{}_y \\rangle^{}$'.format(velocity,velocity, "+"),
               'ax':p[1]},
         'ax2':{'title':'$rms({}_x)^{}$'.format(velocity, "+"), 'ax':p[2]}, 
         'ax3':{'title':'$rms({}_y)^{}$'.format(velocity, "+"), 'ax':p[3], 'ylim':[0, 1]}, 
         'ax4':{'title':'$rms({}_z)^{}$'.format(velocity, "+"), 'ax':p[4], 'ylim':[0, 1]}
    }


    panel(pict_path, data_with_parameters)

