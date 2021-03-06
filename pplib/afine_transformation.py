# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: afine_transformation.py
# Created by: gemusia
# Creation date: 20-01-2018
# Last modified: 18-02-2018 13:22:28
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import numpy as np



def w(U,d1,d2,n):

    # starts with 1
    def interval(i):
        def q1(xi):
            linear_xi =(U[i]-U[i-1] - d1*(U[i+1]-U[i-1]))*xi+ U[i-1]*(1-d1)
            return linear_xi

        def q2(xi):
            linear_xi =(U[i+1]-U[i] - d2*(U[i+1]-U[i-1]))*xi+ U[i]-U[i-1]*d2
            return linear_xi

        def u0(U):
            def u0xi(xi):
                linear_xi =(U[i+1]-U[i-1])*xi+ U[i-1]
                return linear_xi
            return u0xi

        def w_recursive(ui,n):
            def w_xi(xi):
                if xi>=0 and xi<0.5:
                    value = d1*ui(2*xi) + q1(2*xi)   
                    return value
                elif xi>=0.5 and xi<=1:
                    value = d2*ui(2*xi-1) + q2(2*xi-1)   
                    return value
                else:
                    raise ValueError("xi is not in range [0,1]:", xi)

            if n==0:
                return ui 
            else:
                return w_recursive(w_xi,n-1)

        interpolation = w_recursive(u0(U),n)

        return interpolation

    return interval


    
