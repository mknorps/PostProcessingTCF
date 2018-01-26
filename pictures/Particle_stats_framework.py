# import of all the necessary packages

import numpy as np
import matplotlib.pyplot as plt
from os.path import expanduser


# frequently changed constants
StList = ['1','5','25']

file_path    = expanduser("~") + "/results_for_PhD/SGS_model_results/test/"
fig_path     = file_path

ModelLabel='model'
model_type='sgs' # sgs or tot - for fluid velocity at particle position


# declaration of constants

reference_path_LES  = expanduser("~") +"/REFERENCE_DATA/pure_LES/int2/"
reference_path_DNS  = expanduser("~") +"/REFERENCE_DATA/Marchiolli_DATA/TUE/"
DirectionList=['x','y','z']
DirectionList2=['y','z','x']
CommentRows = 58
#CommentRows = 49
CommentRows_LES = 49
CommentRows_DNS = 47
tauplus = 0.0433 
pi = 3.1415

# declaration of picture attributes

StListLineStyle = ['k-^','-o','--','*']

# declaration of variables
data = {}
data_LES = {}
data_DNS = {}



#######################################
# data loading
#######################################

for x in StList:
    #data[x]     = np.loadtxt(file_path + 'particle_stat_3850-3950_' + x +'.0_4', skiprows = CommentRows)
    data[x]     = np.loadtxt(file_path + 'particle_stat_' + x, skiprows = CommentRows)
    data_LES[x] =  np.loadtxt(reference_path_LES +'particle_stat_' + x, skiprows = CommentRows_LES)
    data_DNS[x] = np.loadtxt(reference_path_DNS +'dns_particles_' + x , skiprows = CommentRows_DNS)


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
line_style_dict = {"St1DNS": {"ls":"solid", "color":"blue", "label":"$St1$","lw":2},
                   "St1LES": {"ls":"dashed", "color":"blue","lw":2},
                   "St1model": {"ls":"dotted", "color":"blue","lw":2},
                   "St5DNS": {"ls":"solid", "color":"red", "label":"$St5$","lw":2},
                   "St5LES": {"ls":"dashed", "color":"red","lw":2},
                   "St5model": {"ls":"dotted", "color":"red","lw":2},
                   "St25DNS":{"ls":"solid", "color":"green", "label":"$St25$","lw":2},
                   "St25LES":{"ls":"dashed", "color":"green","lw":2},
                   "St25model":{"ls":"dotted", "color":"green","lw":2}
} 
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

            fig = plt.figure(figsize = (12,9))
            ax0 = plt.subplot2grid((7,2),(0,0),rowspan=4) #ksgs
            ax1 = plt.subplot2grid((7,2),(4,0),rowspan=3) #<Ux,Uy>
            ax2 = plt.subplot2grid((7,2),(0,1),rowspan=3) #rms Ux
            ax3 = plt.subplot2grid((7,2),(3,1),rowspan=2) #rms Uy
            ax4 = plt.subplot2grid((7,2),(5,1),rowspan=2) #rms Uz
            ax = [ax0,ax1,ax2,ax3,ax4]

            for figure in ax:
                figure.set_xlim([1,160])
                figure.set_xscale('log')
                figure.tick_params(axis='both',labelsize=15)
            for figure in [ax3,ax4]:
                figure.set_ylim([0,1.2])
            for figure in [ax1,ax4]:
                figure.set_xlabel("$y^{+}$",fontsize=15)

            ax0.set_title('$k_{sg}^{+}$',fontsize=15)
            ax1.set_title('$\langle '+ velocity +'_x,' + velocity +'_y \\rangle^{+}$',fontsize=15)
            ax2.set_title('$rms('+ velocity +'_x)^{+}$',fontsize=15)
            ax3.set_title('$rms('+ velocity +'_y)^{+}$',fontsize=15)
            ax4.set_title('$rms('+ velocity +'_z)^{+}$',fontsize=15)

            ax0.plot(data_LES[x][:,0],ksgs(data_LES[x],"LES",velocity), **line_style_dict["St"+x+"LES"])
            ax0.plot(data[x][:,0],ksgs(data[x],"model",velocity), **line_style_dict["St"+x+"model"])
            ax0.plot(data_DNS[x][:,0],ksgs(data_DNS[x],"DNS",velocity), **line_style_dict["St"+x+"DNS"])
            for i,subplot in enumerate(ax[1:]):
                subplot.plot(data_LES[x][:,0],data_LES[x][:,col["LES"][i+1]], **line_style_dict["St"+x+"LES"])
                subplot.plot(data[x][:,0],data[x][:,col["model"][i+1]], **line_style_dict["St"+x+"model"])
                subplot.plot(data_DNS[x][:,0],data_DNS[x][:,col["DNS"][i+1]], **line_style_dict["St"+x+"DNS"])

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

        for x in StList:
            for i,subplot in enumerate(ax):
                subplot.plot(data_LES[x][:,0],data_LES[x][:,col["LES"][i]], **line_style_dict["St"+x+"LES"])
                subplot.plot(data[x][:,0],data[x][:,col["model"][i]], **line_style_dict["St"+x+"model"])
                subplot.plot(data_DNS[x][:,0],data_DNS[x][:,col["DNS"][i]], **line_style_dict["St"+x+"DNS"])

        leg = ax0.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(fig_path + velocity + "_concentration_panel_fractal.pdf")
        plt.close(fig)

if __name__=='__main__':

    #velocity_panel()
    #ksgs_panel()
    concentration_panel()
