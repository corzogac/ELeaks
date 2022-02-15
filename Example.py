
#%%
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

# %%
import copy
def createLeak(Nt,node,LeakFlow):
    #Net.remove_pattern('New')
    Net=copy.deepcopy(Nt)
    LeakFlow=[LeakFlow/1000]*(24*1+1)
    Net.options.hydraulic.demand_model = "PDD"
    Net.add_pattern(name ='New', pattern = LeakFlow) #Add New Patter To the model
    Net.get_node(node).add_demand(base= 1, pattern_name='New') #Add leakflow
    Net.options.time.duration = 24*1*3600 #Time of simulation
    return Net    

#%%
def Get_Pattern(Net,node):
    Nt=Net.get_node(node)
    P=Nt.demand_timeseries_list.pattern_list()
    for i in P:
        print(i.name)
        print(i.multipliers)


def RemoveLastPattern(Net,node='141210Y'):
    Nt=Net.get_node(node)
    P=Nt.demand_timeseries_list.pattern_list()
    P.pop(1)
    Nt.demand_timeseries_list=P


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

#print(P)
#Nt=Net1.get_node(Node)
#print(Nt)





#%% 
def GraphNet(Net):
         # wntr.graphics.plot_network(self.OpenNet(), title= 'Network', node_attribute='elevation',node_colorbar_label='Elevation (m)')
         wntr.graphics.plot_interactive_network(
             Net,
             title="Network",
             node_attribute="elevation",
             filename="Elevation.html",
             auto_open=False,
         )
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
            
