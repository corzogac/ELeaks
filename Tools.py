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

    
def Baseline(Net, y = "No_defined"):
    """This function generates a base line information
    1. Identifies and returns position of nodes with zero demand
    2. Returns the base demand 

    Args:
        Net ([Network Object]): [Network Simulated already]
        y (str, optional): [description]. Defaults to "No_defined".

    Returns:
        [BD, MBD, Listnz]: [Three Dataframes, 
        BD is Base Demand
        MBD is Mean Base demand value]
        Listnz  is the list of node names with non zero values
    """
    x = Net
    BD = []
    Listnz=[]
    if y == "No_defined":
        for i in x.junction_name_list:        
            Node = x.get_node(i)
            if Node.base_demand>0:            
                BD.append(Node.base_demand) 
                Listnz.append(Node.name) 
            else:
                BD.append(0)
                
    else:  
        for i in y:
            Node = x.get_node(i)
            if Node.base_demand>0: 
                BD.append(Node.base_demand) 
            else: 
                BD.append(0) 
    BD=np.array(BD)
    MBD=BD.mean()
    
    return BD, MBD, Listnz
