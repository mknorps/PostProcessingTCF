# import of all the necessary packages

import numpy as np
import matplotlib.pyplot as plt
from os.path import expanduser


# frequently changed constants
StList = ['1','5','25']

file_path    = expanduser("~") + "/results_for_PhD/SGS_model_results/FRACTAL/"
#file_path    = expanduser("~") + "/results_for_PhD/test/"
fig_path     = file_path

ModelLabel='model'
model_type='sgs' # sgs or tot - for fluid velocity at particle position


# declaration of constants

reference_path_LES  = expanduser("~") +"/REFERENCE_DATA/pure_LES/int2/"
reference_path_DNS  = expanduser("~") +"/REFERENCE_DATA/Marchiolli_DATA/TUE/"
DirectionList=['x','y','z']
DirectionList2=['y','z','x']
#CommentRows = 58
CommentRows = 49
CommentRows_LES = 49
CommentRows_DNS = 47
tauplus = 0.0433 
pi = 3.1415

# declaration of picture attributes

StListLineStyle = ['k-^','-o','--','*']

# declaration of variables
data = {'LES':{},
        'DNS': {},
        'model': {}
        }



#######################################
# data loading
#######################################

#data["0.2"]     = np.loadtxt(file_path + 'particle_stat_2690-2700_0.2_4', skiprows = CommentRows)
for i,x in enumerate(StList):
    #data[i]     = np.loadtxt(file_path + 'particle_stat_2720-2820_0.2_' + str(i+1) , skiprows = CommentRows)
    data['model'][x]     = np.loadtxt(file_path + 'particle_stat_' + x, skiprows = CommentRows)
    data['LES'][x] =  np.loadtxt(reference_path_LES +'particle_stat_' + x, skiprows = CommentRows_LES)
    data['DNS'][x] = np.loadtxt(reference_path_DNS +'dns_particles_' + x , skiprows = CommentRows_DNS)


#############################################
# Statistics
#  -  mean, rms and covariance on one picture
#############################################

columns = {} # list of columns for mean, correlation and three rms figures
columns['Us'] = {"LES":[24,32,28,29,30],
                 "model":[24,32,28,29,30],
                 "DNS":[11,17,14,15,16] }
columns['Vp'] = {"LES":[2,10,6,7,8],
                 "model":[2,10,6,7,8],
                 "DNS":[2,8,5,6,7] }
columns_concentration = {}
columns_concentration['Us'] = {"LES":[1,32,28,29,30],
                 "model":[1,32,28,29,30],
                 "DNS":[1,17,14,15,16] }
columns_concentration['Vp'] = {"LES":[1,10,6,7,8],
                 "model":[1,10,6,7,8],
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

'''
data_with_parameters:
       - a dictionary containing data and parameters for plots in form of
         dictionaries,
        the main keys are: 'ax0',...'ax4'

        {'ax0':ax0_data, ..., 'ax4':ax4_data}

        ax?_data must contain:
       - 'xlim': [a,b]
       - 'ylim':[a,b]
       - 'xlabel': 'xlabel'
       - 'title' :"plot title"
       - 'ax' : list of dictionaries containing one curve data + plot parameters:
            'x' - x axis data
            'y' - y axis data
            'style' - dictionary of plot style
'''

def panel(data_with_parameters,pict_path):

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
        figure.set_title(data_with_parameters[key]['title'])
        figure.tick_params(axis='both',labelsize=15)
        if data_with_parameters[key]['xlim']:
            figure.set_xlim(data_with_parameters[key]['xlim'],
                            fontsize=15)
        if data_with_parameters[key]['ylim']:
            figure.set_ylim(data_with_parameters[key]['ylim'])
        if data_with_parameters[key]['xlabel']:
            figure.set_xlabel(data_with_parameters[key]['xlabel'],
                              fontsize=15)

    for key,subplot in ax.items():
        for ax_data in data_with_parameters[key]['ax']:
            subplot.plot(ax_data['x'], ax_data['y'],
                         **ax_data['style'])

    leg = ax0.legend(fontsize=15)
    plt.tight_layout()
    fig.savefig(pict_path)
    plt.close(fig)


def axis_parameters():

    axis_params = {}

    return axis_params


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


def ksgs_panel():

    def ksgs(nparray,symulation_type,velocity_type):
        kinetic_energy = 0.5*\
            (nparray[:,columns[velocity_type][symulation_type][2]]**2+\
            nparray[:,columns[velocity_type][symulation_type][3]]**2+\
            nparray[:,columns[velocity_type][symulation_type][4]]**2)

        return kinetic_energy

    for x in StList:
        for velocity,col in columns.items():

            data_with_parameters = {
                 'ax0':{'title':'$k_{sg}^{+}$'},
                 'ax1':{'title':'$\langle '+ velocity +'_x,' + velocity +'_y \\rangle^{+}$'},
                 'ax2':{'title':'$rms('+ velocity +'_x)^{+}$'},
                 'ax3':{'title':'$rms('+ velocity +'_y)^{+}$'},
                 'ax4':{'title':'$rms('+ velocity +'_z)^{+}$'}
            }


            for data_type in ['LES','DNS','model']:
                data_with_parameters['ax0']['x'] = data[data_type][x][:,0]
                data_with_parameters['ax0']['y'] = ksgs(data[data_type][x],data_type,velocity)
                data_with_parameters['ax0']['style'] = line_style_dict["St"+x+data_type]
            panel(data_with_parameters,pict_path)

            leg = ax0.legend(fontsize=15)
            plt.tight_layout()
            fig.savefig(fig_path + velocity +'_St'+x + "_ksgs_panel_log_fractal.pdf")
            plt.close(fig)



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
        fig.savefig(fig_path + velocity + "_concentration_panel_fractal.pdf")
        plt.close(fig)

if __name__=='__main__':

    #velocity_panel()
    #ksgs_panel()
    concentration_panel()
