'''
Created on Sep 9, 2015

@author: sbarnard
'''
import json
from nupic.data.file_record_stream import FileRecordStream
from nupic.engine import Network
from nupic.encoders import MultiEncoder

ATTRIBUTES=["topDownMode", "inferenceMode", "learningMode", "anomalyMode"]

def createNetwork(params):
    network = Network()
    network = createRegions(network, params["poolers"])
    network = createSensors(network, params["sensors"])
    network = addLinks(network, params["links"])
    return network

def createRegions(network, regions):
    for region in regions:
        createRegion(network, region)
    return network
        
def createRegion(network, region):
    r = network.addRegion(name=region["name"], nodeType=region["type"], nodeParams=json.dumps(region["params"]))
    for arg in ATTRIBUTES:
        if arg in region:
            r.setParameter(arg, region[arg])
    return r;       

def createSensors(network, sensors):
    for sensor in sensors:
        dataSource = FileRecordStream(streamID=sensor["source"])
        dataSource.setAutoRewind(True)
        encoder = MultiEncoder()
        encoder.addMultipleEncoders(fieldEncodings=sensor["encodings"])
        s = createRegion(network, sensor)
        s = s.getSelf()
        s.dataSource = dataSource
        s.encoder = encoder
    return network
        
def addLinks(network, links):
    for link in links:
        addLink(network, link)
    return network;


def addLink(network, link):
    network.link(srcName=link["source"], destName=link["destination"], linkType=link["type"], linkParams=link["params"])
    