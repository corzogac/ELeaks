
#%%
from matplotlib.pyplot import get
from Tools import *


#%%
#DirInput='../Start/Networks/'
DirInput='../Start/'

File = DirInput+'network_PDA.inp'  # File used for the model
#File = DirInput+'network_PDA.inp'
#File = 'network_PDA.inp' 
print(File)
Net1=wntr.network.WaterNetworkModel(File)   

#%%
S=RunNet(Net1, "OutputModel/")

print(S)
# %%

BD, MB, Lnz=Baseline(Net1,'OutputModel/')


# %%
for n in Lnz:
    junc=Net1.get_node(n)
    print(f'{n} = {junc.base_demand}')
print(len(Lnz))


# %%
EvaluateLeaks(1,Lnz,Dir='OutputModel/')



#%%
Nod=Net1.node_name_list
Net1.describe()


#%%
#Node='141210Y' 
Node='133487X'
#P=Net1.get_pattern(Node)
Get_Pattern(Net1,Node)
Net2=createLeak(Net1,Node,15)
Get_Pattern(Net2,Node)
#%%
S1=RunNet(Net1, "OutputModel/")
S2=RunNet(Net2, "OutputModel/")



#%%
def percCal(x,y):
  return (x-y)*100/x

def Dif(S1,S2,Node):
    #comparing results of a node
    Df1=S1.node['pressure']
    Df2=S2.node['pressure']

    d=percCal(Df1,Df2)
    v=d[Node].to_numpy()
    R=np.sqrt(np.sum(v**2))/len(v)
    d[Node].plot(kind='density')
    return R

#print(P)
#Nt=Net1.get_node(Node)
#print(Nt)
#%%
#Lnz List of non zero nodes

import time
start_time = time.time()

LeaksNetsList=[]
for i in Lnz:
    #Run 1 network all nodes
    #create Leak at node i
    Net2=createLeak(Net1,i,15)
    LeaksNetsList.append(Net2)


a=time.time() - start_time
print(f'{a} seconds')


#%% 
for i in LeaksNetsList:
    Get_Pattern(i,'133487X')

#%%
def Get_Node(Net,node):
    Nt=Net.node[node]
    P=Nt.demand_timeseries_list.pattern_list()



GraphNet(Net1)



#%% 
def compare(Net1,Net2,Sensor_Nodes,Key='pressure'):
    #dict_keys(['demand', 'head', 'pressure', 'quality'])
    S1=RunNet(Net1,'OutputModel/')
    St = int(Net1.options.time.duration/Net1.options.time.hydraulic_timestep)    
    
    S1 = S1.node[Key].loc[1:St*3600,Sensor_Nodes].\
                rename_axis('Net1',axis=1) # Give name to the dataframe
    S2=RunNet(Net2,'OutputModel/')
    S2 = S2.node[Key].loc[1:St*3600,Sensor_Nodes].\
                rename_axis('Net2',axis=1) # Give name to the dataframe
    
    
    return S2[Sensor_Nodes].sub(S1[Lnz], fill_value=0) # Create divergence matrix 

#%%      
def compareNode(Net1,Net2,Node='133487X',Key='pressure'):
    #dict_keys(['demand', 'head', 'pressure', 'quality'])    
    S1=RunNet(Net1,'OutputModel/')
    St = int(Net1.options.time.duration/Net1.options.time.hydraulic_timestep)    
    
    S1 = S1.node[Key].loc[1:St*3600,Sensor_Nodes].\
                rename_axis('Net1',axis=1) # Give name to the dataframe
    S2=RunNet(Net2,'OutputModel/')
    S2 = S2.node[Key].loc[1:St*3600,Sensor_Nodes].\
                rename_axis('Net2',axis=1) # Give name to the dataframe
    
    D=S2[Node].sub(S1[Node], fill_value=0)
    
    return sum(D)  # Create divergence matrix 
            
