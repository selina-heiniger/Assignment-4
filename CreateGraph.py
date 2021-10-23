# -*- coding: utf-8 -*-
"""
Developed by:
Moin Khan
Adapted by:
Selina Heiniger
Python 3.8
---
Plots stress-strain graph
"""

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.offsetbox import AnchoredText

#%% plotGraph function

def plotGraph(Strain, Stress, StrainValuesLinear, StrainValuesEng, StrainValuesTrue, f1, f2, f3, uts,
              LinearLimit, Modulus, ElasticLimit, failureStress):
    
    fig = plt.figure()                                              # creates plot window
    ax = fig.add_subplot(1,1,1)
    
    ax.plot(Strain,Stress, 'o')                                  # plots values from testing
    ax.plot(StrainValuesLinear, f1(StrainValuesLinear),'b-')     # plots linear part of graph
    ax.plot(StrainValuesEng, f2(StrainValuesEng),'g-')           # plots interpolation line of test results
    ax.plot(StrainValuesTrue, f3(StrainValuesTrue),'r-')         # plots interpolation line of corrected test results

    # Label
    ax.set_xlabel('Strain')
    ax.set_ylabel('Stress  (MPa)')



    # UTS Line
    plt.axhline(y=uts, ls=':', c='cyan')                            # plots horizontal line through UTS
    # Ductility Line
    plt.axvline(x=Strain[-1], ls=':', c='purple')                   # plots vertical line through UTS

    # Offset Line
    xA = [Strain[0],Strain[LinearLimit]]                                    # defines points through linear part
                                                                            # between 0 and linear limit in X
    yA = [Stress[0],Stress[LinearLimit]]                                    # defines points through linear part
                                                                            # between 0 and linear limit in Y
    StrainValuesOffset = [x +.002*Strain[-1] for x in xA]                   # creates points slightly offset
                                                                            # from linear strain line (offset line)
    f4 = interp1d(StrainValuesOffset, yA, fill_value='extrapolate')         # creates interpolation line for 
                                                                            # offset part of the linear plot
    StrainValuesOffset.append(Strain[LinearLimit+1])                        # adds additional point to offset
                                                                            # line to extend it
    ax.plot(StrainValuesOffset,f4(StrainValuesOffset),':',color='orange')   # plots offest line


    # Offset yield value              
    val=Strain[LinearLimit]                                     # defines strain at yield point (LinearLimit)
    step = (Strain[LinearLimit+1]-Strain[LinearLimit])/50       # defines step size for while loop (below)                             

    while((f4(val)-f2(val)) <= 0):                              # searches for position where
        val += step                                             # offset curve crosses the non-linear
                                                                # uncorrected line. starting at Linear Limit
                                                                # and moving up in small steps

    YieldPoint = f4(val-step)                                   # Defines YieldPoint through position that 
                                                                # was defined in while loop

    plt.axhline(y=YieldPoint, ls=':', c='black')                # plots horizontal line through YielPoint


    # Legend
    plt.legend(['Actual Values', 'Linear Region ', 'Engineering Stress Strain',
                'True Stress Strain','UTS','Max Strain','Offset Line','Yield Point'], loc='best')
                                                                # plots legend of graph
    # Anchor
    anchoredText = AnchoredText("Young's Modulus = " +"%.5f" % Modulus + " GPa\n" 
                                 + "Elastic Limit = " + "%.5f" % ElasticLimit + " MPa\n" 
                                 + "Yield Stress = "+ "%.5f" % YieldPoint + " MPa\n"
                                 + "UTS = "+ "%.5f" % uts +" MPa\n"
                                 + "Failure Stress = " + "%.5f" % failureStress +" MPa\n"
                                 + "Max Strain = "+ "%.5f" % Strain[8], loc='right')
                                    # creates Anchor for curve properties
                                    
    ax.add_artist(anchoredText)     # prints Anchor

    # Axis Limits
    ax.set_xlim(xmin=0)             # sets axis minimum limit to 0 for x axis
    ax.set_ylim(ymin=0)             # sets axis minimum limit to 0 for y axis

    # Display graph
    plt.show()                      # displays plot window