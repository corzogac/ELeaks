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
import time
import wntr
import pickle
import numpy as np


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



def EvaluateLeaks(RN=1,Lnz=''):
    """[summary]

    Args:
        RN (int, optional): [description]. Defaults to 1.
        DirPath (str, optional): [description]. Defaults to 'test'.
        Lnz (str, optional): [description]. Defaults to ''.
    
    Result: Stores the result ina DF in the 
    """
    
    nd=1
    DirPath='OutputModel'

    start = time.time()  #start of the Timer, just for evaluate code performance. 
    #print(start)   
    
    f=open(DirPath+'wn.pkl','rb')
    Net=pickle.load(f)
    f.close()

    f=open(DirPath+'ns.pkl','rb')
    Net_Sim=pickle.load(f)
    f.close()


    Net.options.hydraulic.demand_model=Method   #Using PDD as demand method
    Net.options.time.duration = nd*24*3600    #Time of simulation
    
    St = int(Net.options.time.duration/Net.options.time.hydraulic_timestep)    

    #Base pressures
    BPM = Net_Sim.node['pressure'].loc[1:St*3600,Net.junction_name_list] 
    BPM=BPM[Lnz]

    LPM = []        #Leak pressure matrix        
    LM = []         #Leakage Matrix
    DM = []         #Divergence matrix
    R={}
    
    Leak_Nodes = Lnz #(Net.junction_name_list 
    Sensor_Nodes = Lnz 
    print(len(Leak_Nodes))
    print(len(Sensor_Nodes))
    Leakmin=Run/100
    Leakmax=(Run+1)/100
    #dl=(Leakmax-Leakmin)/10
    LeakFlows = np.arange(Leakmin,Leakmax,0.001)

    for i in Leak_Nodes:   
        start2 = time.time()     
        for k in range(len(LeakFlows)):  
            #__________________      
            LeakFlow = [LeakFlows[k]/1000]*(24*nd+1) #array of the leak flow (m3/s)         
            f=open(DirPath+'wn.pkl','rb')
            Net=pickle.load(f)
            f.close()
            Net.add_pattern(name ='New', pattern = LeakFlow) #Add New Patter To the model
            Net.get_node(i).add_demand(base= 1, pattern_name='New') #Add leakflow
            Net.options.time.duration = 24*nd*3600 #Time of simulation
            #print(f'before run leak node no={i}, leak flow{k}')
            Net_New = RunNet(Net,DirPath) # Run new model 
            #__________________________________________
            #   
            Net2 = Net_New.node['pressure'].loc[1:St*3600,Sensor_Nodes].\
                rename_axis('Node_'+i+', '+str(round(LeakFlows[k],2))+'LPS',axis=1) # Give name to the dataframe
            LPM.append(Net2[Lnz]) # Save pressure results
            
            Difference = BPM[Sensor_Nodes].sub(Net2[Lnz], fill_value=0) # Create divergence matrix 
            
            DM.append(Difference.abs().rename_axis('Node_'+ i+', '\
                +str(round(LeakFlows[k],2))+'LPS', axis=1)) # Save Divergence M.                             
            
            lf=pd.DataFrame([k*1000 for k in LeakFlow[1:]], columns = ['LeakFlow']\
                , index =list(range(3600,St*3600+3600,3600))).\
                rename_axis('Node: ' + i, axis=1)
            LM.append(lf) #Save leakflows used

            print(f'leakflow = {k} and value {LeakFlows[k]}, LeakNode={i}')
        print('____**____')
        print(f'All leaks nodes {i} Time= {time.time()-start2}')
        R['LPM']=LPM
        R['DM']=DM
        R['LM']=LM

        f=open("/scratch-shared/tmp.gJSE36s506/output/"+'DF_'+str(Run)+'_'+str(i)+'.pkl','wb')
        pickle.dump(R,f)
        f.close()
    print(f'Finish Time 1= {time.time()-start}')    
    TM_ = []   # time when the leak was identified
    WLM = []   # Water loss Matrix (L/s), how much water is wasted
      

    for i in range(len(DM)):    
        TMtemp = [] 
        WLMtemp = []
        for j in Sensor_Nodes:
            WLMtemp2 = [] 
            for k in range(len(DM[0])):
                if DM[i][j][(k+1)*3600] <= Threshold:                
                    WLMtemp2.append(LM[i].LeakFlow[(k+1)*3600]*3600)              
                else:                
                    WLMtemp2.append(LM[i].LeakFlow[(k+1)*3600]*3600)
                    break
            TMtemp.append(k+1)
            WLMtemp.append(sum(WLMtemp2))        
        TM_.append(TMtemp)
        WLM.append(WLMtemp)
    print(f'Finish Time 2= {time.time()-start2}')  
    R={}
    R['LPM']=LPM
    R['DM']=DM
    R['LM']=LM
    R['Meta']={'Leakmin':Leakmin,'Leakmax':Leakmax,'Run':Run,'Run Time':time.time()-start2}
    R['TM_l']=TM_
    R['WLM']=WLM
    return R