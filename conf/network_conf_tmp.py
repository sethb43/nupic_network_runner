'''
Created on Sep 9, 2015

@author: sbarnard
'''
NETWORK_PARAMS={"poolers":[
                           {"name":"spRegion",
                            "type":"py.SPRegion",
                            "learningMode":True,
                            "anomalyMode":True,
                            "params": {  'columnCount': 2048,
                                         'globalInhibition': 1,
                                         'inputWidth': 2400,
                                         'maxBoost': 2.0,
                                         'numActiveColumnsPerInhArea': 42,
                                         'potentialPct': 0.8,
                                         'potentialRadius': 32,
                                         #'stimulusThreshold': 5,
                                         'seed': 1901,
                                         'spVerbosity': 0,
                                         'spatialImp': 'cpp',
                                         'synPermActiveInc': 0.05,
                                         'synPermConnected': 0.1,
                                         'synPermInactiveDec': 0.0121}
                            },
                           {"name":"tpRegion",
                            "type":"py.TPRegion",
                            "topDownMode":True,
                            "inferenceMode":True,
                            "learningMode":True,
                            "anomalyMode":True,
                            "params": { 'activationThreshold': 12,
                                         'cellsPerColumn': 1,
                                         'columnCount': 2048,
                                         'globalDecay': 0.0,
                                         'initialPerm': 0.21,
                                         'inputWidth': 2048,
                                         'maxAge': 0,
                                         'outputType': 'activeState',
                                         'permanenceDec': 0.1,
                                         'permanenceInc': 0.1,
                                         'seed': 1910,
                                         'temporalImp': 'cpp',
                                         'verbosity': 0, 
                                         'outputType' : 'normal' }
                            }
                           ],
                "sensors":[
                           {"name":"sensor1",
                            "params":{ 'verbosity': 0 },
                            "type":"py.RecordSensor",
                            "encodings":{ 'TRACTOR_PPG':     { 'name': 'TRACTOR_PPG', 'fieldname': 'FMDL_SC_TR_TRACTOR_PPG', 'resolution': 0.001, 'type': 'RandomDistributedScalarEncoder' }},
                            "source":"./Swift3.csv"
                            }
                           ],
                "links":[
                         {"source":"sensor1",
                          "destination":"spRegion",
                          "type":"UniformLink",
                          "params":""
                          },
                         {"source":"spRegion",
                          "destination":"tpRegion",
                          "type":"UniformLink",
                          "params":""
                          }
                         ]
                }