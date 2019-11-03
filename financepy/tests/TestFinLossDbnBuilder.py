# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 17:54:58 2019

@author: Dominic O'Kane
"""

import sys
sys.path.append("..//..")

import time
import numpy as np
import matplotlib.pyplot as plt

from financepy.models.FinGaussianCopula1FModel import lossDbnHeterogeneousAdjBinomial
from financepy.models.FinGaussianCopula1FModel import lossDbnRecursionGCD

from financepy.finutils.FinTestCases import FinTestCases, globalTestCaseMode
testCases = FinTestCases(__file__,globalTestCaseMode)

################################################################################

def test_FinLossDbnBuilder():
                
    numCredits = 125
    
    x = np.linspace(0,numCredits,numCredits+1)
    defaultProb = 0.30
    numIntegrationSteps = 25
    lossUnits = np.ones(numCredits) 
    lossRatio = np.ones(numCredits) 

    testCases.header("BETA","BUILDER","LOSS0","LOSS1","LOSS2","LOSS3","TIME")   

    for beta in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]:    

        defaultProbs = np.ones(numCredits) * defaultProb
        betaVector = np.ones(numCredits) * beta    

        start = time.time()            

        dbn1 = lossDbnRecursionGCD(numCredits, 
                                   defaultProbs, 
                                   lossUnits, 
                                   betaVector, 
                                   numIntegrationSteps)        

        end = time.time()

        testCases.print(beta,"FULL_GCD",dbn1[0],dbn1[1],dbn1[2],dbn1[3],end-start)

        ########################################################################
        
        start = time.time()
        dbn2 = lossDbnHeterogeneousAdjBinomial(numCredits, 
                                               defaultProbs, 
                                               lossRatio, 
                                               betaVector, 
                                               numIntegrationSteps)        
        end = time.time()
 
        testCases.print(beta,"ADJ_BIN",dbn2[0],dbn2[1],dbn2[2],dbn2[3],end-start)

        ########################################################################
        
        if 1==0:
            plt.figure()
            plt.plot(x,dbn1,label='GCD FULL')
            plt.plot(x,dbn2,label='ADJ BIN')
            plt.legend()
            plt.show()
    
            dbn3 = dbn2-dbn1
            plt.plot(x,dbn3,label='DIFF')
            plt.legend()
            plt.show()

################################################################################
        
test_FinLossDbnBuilder()
testCases.compareTestCases()