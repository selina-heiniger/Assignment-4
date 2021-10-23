'''
Developed by:
Moin Khan
Adapted by:
Selina Heiniger
Python 3.8
---
Plots yield curve for given Force and elongation input
'''

import numpy as np
import math
from scipy.interpolate import interp1d
import ImportData
import CreateGraph


#%% Input values

data = "C:/Users/Selina Heiniger/Documents/GitHub/Stress-Strain-Curve/Input-data.csv"
# Defines the path of the data file from the stress-strain tests. 

Force = ImportData.getForce(data)                  # calls function to import the force data, force given in gram
Elongation = ImportData.getElongation(data)        # calls fucntion to import the deformation data

GLength = 75                                        # length of the sample
Radius = 6.65                                       # radius of the sample 
LinearLimit = 1                                     # position of point through which linear line will pass 


#%% Properties of stress-strain plot

# Area 
Area = math.pi*Radius**2                             # calculates area of the sample

# Stress and strain
Stress = [ (x*9.81)/Area for x in Force ]           # stress = force / area, factor 9.81 to transform force
                                                    # from g to kN
Strain = [ x/GLength for x  in Elongation ]         # strain = deformation / total length

# True Stress
TrueStress = [ x * (1+y) for y,x in zip(Strain,Stress)]     # TrueStress = (1+strain) * stress
                                                            # cross section correction
#True Strain 
TrueStrain = [math.log(1+x) for x in Strain]                # TrueStrain = ln(1+strain)
                                                            # final length correction

#Values needed for interpolation

StrainValuesLinear = np.linspace(Strain[0], Strain[LinearLimit], num=41, endpoint=True)   
# Creates strain values for the plot for linear part of the plot

StrainValuesEng = np.linspace(Strain[LinearLimit], Strain[-1], num=41, endpoint=True)
# Creates strain values for the plot for the non-linear strain measured (without corrections)

StrainValuesTrue = np.linspace(TrueStrain[LinearLimit], TrueStrain[-1], num=41, endpoint=True)
# Creates strain values for the plot for the non-linear strain that was corrected (with corrections)

#Interpolation
f1 = interp1d(Strain, Stress, fill_value='extrapolate')             
# creates interpolation line for linear part of the plot
f2 = interp1d(Strain, Stress, kind=3, fill_value='extrapolate')     
# creates interpolation line for non-linear non-corrected part of the plot
f3 = interp1d(TrueStrain, TrueStress, kind=3)
# creates interpolation line for non-linear corrected part of the plot


#%% Limits and elastic modulus

# Elastic limit
ElasticLimit = Stress[LinearLimit]                          # elastic limit is defined by the stress 
                                                            # at the position of LinearLimit (defined above)
# Modulus
Slope = Stress[LinearLimit]/Strain[LinearLimit]             # Slope of linear part = Stress / Strain
Modulus = Slope/math.pow(10,3)                              # Modulus in GPa

uts = max(Stress)                                           # Ultimate Tensile Strength is defined as the
                                                            # maximum stress a material can withstand
# Failure Stress
failureStress = f2(max(Strain))                             # Failure stress is assumed at the maximum
                                                            # of the non-corrected stress curve

#%% Plot
CreateGraph.plotGraph(Strain, Stress, StrainValuesLinear, StrainValuesEng, StrainValuesTrue, f1, f2, f3, uts,
              LinearLimit, Modulus, ElasticLimit, failureStress) # calls function to create graph



