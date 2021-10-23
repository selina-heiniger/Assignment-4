# -*- coding: utf-8 -*-
"""
Developed by:
Moin Khan
Adapted by:
Selina Heiniger
Python 3.8
---
Reads Input Data for Force and Elongation measurements
"""

import pandas as pd # package needed for import function

def getForce(path):
    """ Imports Force vector from document in given path"""
    data = pd.read_csv(path,sep=";")    
    return data.Force
 
def getElongation(path):
    """ Imports Elongation vector from document in given path"""
    data = pd.read_csv(path,sep=";")
    return data.Elongation





