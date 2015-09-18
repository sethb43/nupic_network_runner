NETWORK_PARAMS={"poolers":[
                           {"name":"spReg1", 
                            "type":"py.SPRegion",
                            "learningMode":True,
                            "anomalyMode":True,
                            "params": { 'columnCount': 2048,
                                 'globalInhibition': 1,
                                 'inputWidth': 1200,
                                 'maxBoost': 3,
                                 'numActiveColumnsPerInhArea': 40,
                                 'potentialPct': 0.6,
                                 'potentialRadius': 16,
                                 'globalInhibition': 1,
                                 'seed': 1926,
                                 'spVerbosity': 0,
                                 'spatialImp': 'cpp',
                                 'synPermActiveInc': 0.05,
                                 'synPermConnected': 0.1,
                                 'synPermInactiveDec': 0.0125}
                            },
                           {
                            "name":"tpReg1",
                            "type":"py.TPRegion",
                            "topDownMode":True,
                            "inferenceMode":True,
                            "learningMode":True,
                            "anomalyMode":True,
                            "params": { 'activationThreshold': 12,
                                 'cellsPerColumn': 32,
                                 'columnCount': 2048,
                                 'initialPerm': 0.21,
                                 'inputWidth': 2048,
                                 'globalDecay': 0.0,
                                 'maxAge': 0,
                                 #'maxSegmentsPerCell': 128,
                                 #'maxSynapsesPerSegment': 32,
                                 #'minThreshold': 10,
                                 #'pamLength': 1,
                                 'newSynapseCount': 20,
                                 'permanenceDec': 0.1,
                                 'permanenceInc': 0.1,
                                 'seed': 1932,
                                 'temporalImp': 'cpp',
                                 'verbosity': 0}
                            }
                           ],
                "sensors":[        
                           {"name":"CostSensor",
                            "params":{ 'verbosity': 0 },
                            "type":"py.RecordSensor",
                           "encodings":{ 'TRACTOR_COST':  { 'name': 'TRACTOR_COST', 'fieldname': 'FMDL_SC_TR_TRACTOR_COST', 'resolution': 5.0, 'type': 'RandomDistributedScalarEncoder' }, 
                                        'PPG_NR2':    { 'name': 'PPG_NR2', 'fieldname': 'FMDL_RETAIL_PPG_NR2', 'resolution': 0.01, 'type': 'RandomDistributedScalarEncoder' } ,
                                        'SC_DISCOUNT':   { 'name': 'SC_DISCOUNT', 'fieldname': 'FMDL_RD_SC_SELECT_DISCOUNT', 'resolution': 0.5, 'type': 'RandomDistributedScalarEncoder' }
                                        },
                            "source":"./SecondPass.csv"
                            }
                           ],
                "links":[
                         #SP to tp Top
                         {"source":"spReg1",
                          "destination":"tpReg1",
                          "type":"UniformLink",
                          "params":""
                          },  
                         
                         #Sensors to SPs                      
                         {"source":"CostSensor",
                          "destination":"spReg1",
                          "type":"UniformLink",
                          "params":""
                          }
                         ]
                }