'''
Created on Sep 9, 2015

@author: sbarnard
'''
import os
import sys
sys.path.append(os.getcwd()+"/..")
from network import hierarchy_generator as generator
from conf.network_conf import NETWORK_PARAMS
from utils import nupic_anomaly_output as nupic_output
import copy
from nupic.algorithms.anomaly import computeRawAnomalyScore

def runNetwork(network, numIterations):

    network.initialize()
    
    prevPredictedColumns = []
    # Run the network showing current values from sensors and their anomaly scores
    output = nupic_output.NuPICPlotOutput(["Anomaly Scores"])
    
    for i in range(numIterations):
        network.run(1)      
        
        if i == 2000:
            for p in NETWORK_PARAMS["poolers"]:
                network.regions[p["name"]].setParameter("learningMode", False)

        spNode = network.regions["spTopRegion"]
        tpNode = network.regions["tpTopRegion"]
        
        # The anomaly score is relation of active columns over previous predicted columns
        activeColumns = spNode.getOutputData("bottomUpOut").nonzero()[0]
        anomalyScore = computeRawAnomalyScore(activeColumns, prevPredictedColumns)

        print anomalyScore
        output.write(i, anomalyScore)
        #print currTime, 0, anomalyScore

        predictedColumns = tpNode.getOutputData("topDownOut").nonzero()[0]
        prevPredictedColumns = copy.deepcopy(predictedColumns)
            
    output.close()


if __name__ == "__main__":
    network = generator.createNetwork(NETWORK_PARAMS)

    numIterations = input("Type the number of iterations: ")

    runNetwork(network, numIterations)
