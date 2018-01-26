# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
import matplotlib.pyplot as plt
from os.path import expanduser


Ux = np.array([ 0.010456  ,  0.016766  ,  0.028213  ,  0.030915  ,  0.021598  ,0.017541  ,  0.022338  ,  0.032532  ,  0.046086])

file_path    = expanduser("~") + "/results_for_PhD/fractal/"
fig_path     = file_path


def line_from_points(x,y):
    
    try:
        a = (y[0]-y[1])/(x[0]-x[1])
    except ZeroDivisionError:
        print("points form a vertical line")
    b = y[0]-a*x[0]

    def line(x):
        y = a*x+b
        return y

    return line

def max_vertical_distance(points,values,line):

    distance = [(x,line(x)-values[i]) for i,x in enumerate(points)]

    dist = max(distance, key=lambda y: abs(y[1]))

    return dist



def draw(lines,pict_path):

    fig = plt.figure(figsize = (6,4))
    ax1 = plt.subplot2grid((1,1),(0,0)) #tme_xx

    ax1.yaxis.set_ticklabels([])
    ax1.yaxis.set_ticks([])
    ax1.set_xlabel("$x$",fontsize=15)
    ax1.set_ylabel("$U_{x}$",fontsize=15)
    #ax1.set_xlim([0,2*np.pi])
    #ax1.set_ylim([0,np.pi])

    l = len(lines)
    line_02 = line_from_points((0,l-1),(lines[0],lines[l-1]))
    line_01 = line_from_points((0,l//2),(lines[0],lines[l//2]))
    line_12 = line_from_points((l//2,l-1),(lines[l//2],lines[l-1]))

    dt = max_vertical_distance(range(l),lines,line_02)
    d0 = max_vertical_distance(range(l//2+1),lines[:l//2+1],line_01)
    d1 = max_vertical_distance(range(l//2,l),lines[l//2:],line_12)

    ax1.plot(lines,'.',label="target", color='black')
    ax1.plot([0,l//2,l-1],[lines[0],lines[l//2],lines[l-1]],'o',label="fixed", color='red')
    ax1.plot([0,l-1],[lines[0],lines[l-1]],ls='solid',color='black')
    ax1.plot([0,l//2,l-1],[lines[0],lines[l//2],lines[l-1]], color='blue')


    ax1.vlines(dt[0], lines[dt[0]],lines[dt[0]]+dt[1], linestyle='dashed',lw=1)
    ax1.vlines(d0[0], lines[d0[0]],lines[d0[0]]+d0[1], linestyle='dashed',color='blue', lw=1)
    ax1.vlines(d1[0], lines[d1[0]],lines[d1[0]]+d1[1], linestyle='dashed',color='blue', lw=1)

    ax1.text(dt[0]+0.1, lines[dt[0]]+0.5*dt[1], "$d$")
    ax1.text(d0[0]-0.3, lines[d0[0]]+0.5*d0[1], "$d_{1}$")
    ax1.text(d1[0]+0.1, lines[d1[0]]+0.5*d1[1], "$d_{2}$")

    leg = ax1.legend(fontsize=15)
    plt.tight_layout()#
    fig.savefig(pict_path )
    plt.close(fig)

if __name__=='__main__':

    pic_path = fig_path+"stretching_params.pdf"
    
    draw(Ux,pic_path)
