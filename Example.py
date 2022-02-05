from Tools import *

DirInput=''
File = DirInput+'network_PDA.inp'  # File used for the model
#File = 'network_PDA.inp' 
print(File)
Net1=wntr.network.WaterNetworkModel(File)   


S=RunNet(Net1, "OutputModel/")

print(S)