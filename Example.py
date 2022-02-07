#%%
from Tools import *


#%%
DirInput='../Networks/'
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
    print(junc.base_demand)
print(len(Lnz))


# %%
EvaluateLeaks(1,Lnz,Dir='OutputModel/')
# %%
