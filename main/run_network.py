'''
Created on Sep 9, 2015

@author: sbarnard
'''
from network import hierarchy_generator as generator
from conf.network_conf import NETWORK_PARAMS
from utils import nupic_output
import datetime
import copy
from nupic.algorithms.anomaly import computeRawAnomalyScore

def runNetwork(network, numIterations):

    network.initialize()
    
    # Only encodings with "EnableInference" turned "ON" will be printed
    links = { "sensorName": "sensor1", "regionName": "tpRegion", "encodings": [["TRACTOR_PPG", 2], ], "prevPredictedColumns": [] }
    
    # Run the network showing current values from sensors and their anomaly scores
    output = nupic_output.NuPICPlotOutput(["Anomaly Scores"])
    
    for i in range(numIterations):
        network.run(1)      
        
        if i == 50:
            for p in NETWORK_PARAMS["poolers"]:
                network.regions[p["name"]].setParameter("learningMode", False)
        

        regionName = links["regionName"]
        prevPredictedColumns = links["prevPredictedColumns"]
        spNode = network.regions[regionName]
        tpNode = network.regions[regionName]
        
        # The anomaly score is relation of active columns over previous predicted columns
        activeColumns = spNode.getOutputData("bottomUpOut").nonzero()[0]
        anomalyScore = computeRawAnomalyScore(activeColumns, prevPredictedColumns)
        if anomalyScore>.05:
            anomalyScore = anomalyScore-.05
        else:
            anomalyScore = .05;
        currTime = datetime.datetime.now()
        output.write([currTime], [.05], [anomalyScore])

        predictedColumns = tpNode.getOutputData("topDownOut").nonzero()[0]
        links["prevPredictedColumns"] = copy.deepcopy(predictedColumns)
            
    output.close()


if __name__ == "__main__":
    network = generator.createNetwork(NETWORK_PARAMS)

    numIterations = input("Type the number of iterations: ")

    runNetwork(network, numIterations)