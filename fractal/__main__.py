# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: __main__.py
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pplib import options
from pplib import afine_transformation as at


Ufx_short = np.array([ 0.020883 ,  0.021884 ,  0.036644 ,  0.025015 ,  0.031795])
Ufx = np.array([ 0.020883 ,  0.021884 ,  0.036644 ,  0.025015 ,  0.031795 ,
       -0.013087 , -0.017833 , -0.010748 , -0.01598  , -0.025252 ,
       -0.029198 ,  0.015406 , -0.0037895,  0.012066 ,  0.0084922,
       -0.022047 , -0.0069716,  0.010472 ,  0.0055341, -0.011386 ,
       -0.0071907,  0.0072798, -0.013713 , -0.028218 , -0.007487 ,
       -0.018993 , -0.013928 ,  0.012961 ,  0.014386 ,  0.0098586,
       -0.0049017,  0.011529 ])

Ux = np.array([ 0.010456  ,  0.016766  ,  0.028213  ,  0.030915  ,  0.023598  ,
        0.018541  ,  0.022338  ,  0.032532  ,  0.046086  ,  0.052497  ,
        0.033406  ,  0.010971  ,  0.017257  ,  0.028129  ,  0.03444   ,
        0.038584  ,  0.035648  ,  0.026684  ,  0.015635  ,  0.0034943 ,
       -0.014758  , -0.028788  , -0.027637  , -0.024922  , -0.021698  ,
       -0.017567  , -0.0086551 , -0.00042793, -0.00034159, -0.0080953 ,
       -0.013032  , -0.035006  , -0.033873  , -0.0097744 ,  0.00014538,
       -0.010529  , -0.021898  , -0.033015  , -0.037384  , -0.039061  ,
       -0.047662  , -0.052705  ,  0.010853  ,  0.059294  ,  0.029961  ,
        0.0041287 , -0.0055867 , -0.0080131 , -0.0070568 , -0.0030375 ,
        0.0029349 ,  0.0076756 ,  0.017097  ,  0.022855  ,  0.017541  ,
        0.0061875 ,  0.0041762 ,  0.0052054 , -0.0038808 , -0.018172  ,
       -0.012015  , -0.020332  , -0.034864  , -0.043307  , -0.0099216 ,
        0.024673  ,  0.020278  ,  0.017703  ,  0.0039129 , -0.00036879,
        0.0017766 ,  0.007711  ,  0.010874  ,  0.0069801 ,  0.00089039,
       -0.00064433, -0.013879  , -0.020836  , -0.024862  , -0.01705   ,
       -0.0064518 ,  0.0039027 ,  0.0076543 ,  0.011447  ,  0.011387  ,
        0.0040348 , -0.0031128 , -0.01177   , -0.019913  , -0.019688  ,
       -0.017569  , -0.017869  , -0.024573  , -0.038373  , -0.043589  ,
       -0.020853  ,  0.0079963 ,  0.011965  ,  0.0032456 , -0.010713  ,
       -0.027428  , -0.04607   , -0.044556  , -0.0031629 ,  0.0041793 ,
       -0.0025509 , -0.0061638 ,  0.0051976 ,  0.012456  ,  0.016649  ,
        0.017583  ,  0.017353  ,  0.017582  ,  0.01454   ,  0.010906  ,
        0.010808  ,  0.011209  ,  0.0086796 ,  0.0029279 ,  0.005537  ,
       -0.0054026 , -0.023176  , -0.0092315 ,  0.010115  ,  0.024509  ,
        0.025849  ,  0.020879  ,  0.011305  ])


def draw_fractal(pict_path,*df_args,label={}):

    if label == {}:
        label={i:str(i) for i in range(len(df_args))}
    fig = plt.figure(figsize = (12,6))
    ax1 = plt.subplot2grid((1,1),(0,0)) 

    ax1.xaxis.set_ticklabels([1,2,3,4,5])
    ax1.xaxis.set_ticks([0,4,8,12,16])
    ax1.yaxis.set_ticks([])
    ax1.yaxis.set_ticklabels([])
    ax1.set_ylabel("$U_{x}$",fontsize=15)
    ax1.set_xlabel("node number",fontsize=15) 


    #filtered_x = np.arange(32)*4
    #ax1.plot(Ux,label="DNS",lw=1)
    #ax1.plot(filtered_x,Ufx,label="apriori",lw=2)
    #ax1.plot(filtered_x[:8],Ufx[:8],label="apriori",lw=2)

    for i,df in enumerate(df_args):
        ax1.plot(df["x_norm"],df["y"],label = label[i],lw=2**(3-i))

    leg=ax1.legend()
    plt.tight_layout()
    fig.savefig(pict_path )
    plt.close(fig)


def fractal_interpolation(ui):
    x = []
    y = []
    samples=np.arange(0,1,0.0005)

    #samples = np.random.random_sample((75,))
    for s in samples:
        for i in range(1,len(Ufx_short)-1,2):
            interpolated = ui(i)(s) #one point
            x.append(s*2+i-1)
            y.append(interpolated)
    fractal = pd.DataFrame({"x":x,"y":y})
    fractal["x_norm"] = fractal["x"]*4
    fractal.sort_values("x_norm", inplace=True)

    return fractal

def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    y = parsed_args.slice_yplus

    d1 = 2**(-1/3)   
    d2 = 2**(-1/3)    

    interpolated_w1 =fractal_interpolation(at.w(Ufx,d1,d2,3)) 

    draw_fractal("test.pdf", interpolated_w1)

    w0 =fractal_interpolation(at.w(Ufx_short,d1,d2,0)) 
    w1 =fractal_interpolation(at.w(Ufx_short,d1,d2,1)) 
    w2 =fractal_interpolation(at.w(Ufx_short,d1,d2,2)) 
    w3 =fractal_interpolation(at.w(Ufx_short,d1,d2,3)) 
    w8 =fractal_interpolation(at.w(Ufx_short,d1,d2,8)) 
    label = {i:'$W^{'+str(i+1)+'}$' for i in range(4)}
    label[3] = '$W^{8}$'
    draw_fractal("W_levels_2.pdf", w1,w2,w3,w8,label=label)

if __name__=="__main__":

    run_project(sys.argv)

