""" Modules to run and extract data from a EPANET model
Usage:
    ./Tools.py

Author:
    Gerald Corzo
Date:02/07/2022

Acknoledgements: Work developed with the support of 
- Andres Lopez Garcia 
- Leonardo Alfonso Segura


"""

import wntr


def RunNet (x, OutPath):
    """RunNet is a function that simulates a network
    receive a FileNam and a Path to store the outputs 

    Args:
        x ([Network Object from WNTR]): [A network file read
        with wntr.network.WaterNetworkModel(<FileName>) ]
        OutPath ([Path String]): [Location to store the results]

    Returns:
        Sim [network simulated]: [Generates outpus in the output path]
        
                 Type= wntr.sim.results.SimulationResults object 
    """
    sim = wntr.sim.EpanetSimulator(x)
    if OutPath=='':        
        pre=OutPath+'temp'
    else:
        pre=OutPath+'/temp'

    sim = sim.run_sim(version=2.2,file_prefix=pre ) 
    return sim