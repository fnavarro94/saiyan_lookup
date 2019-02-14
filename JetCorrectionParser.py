import uproot, uproot_methods
import numpy as np

filePath = "files/test.txt"
f = open(filePath, 'r').readlines()


bins = [] #contains bin values
binsTemp = [] # used to build bins variable
binParameters = [] # names of the expected parameters used for bin lookup
functionParameters = [] # names of the expected parameters required to evaluate the function

possibleCorrections = ['L1FastJet','L2Relative','L3Absolute']


params_raw = f[0].strip().strip('{').strip('}').split()
params_raw[0].strip('{')
params_raw[len(params_raw)-1].strip('}')
params = params_raw

num_binParams = int(params[0])
num_funcParams = int(params[num_binParams + 1])
num_allParams = num_binParams + num_funcParams
num_tableFuncParams = int(f[1].split()[num_binParams*2])-num_funcParams*2
function = params[2+num_funcParams+num_binParams]

for n in range(1,num_binParams + 1):
	binParameters.append(params[n])
for n in range(num_binParams +2,num_binParams+num_funcParams+2):
	functionParameters.append(params[n])

# Function parameters limits dictionary
funcParamLimits_dict = {}
funcParamLimits_vec = []
tableFuncParams = []

for n, line in enumerate(f):
	tableFuncParams_temp = []
	if n==0 or line=='\n':
		continue
	else:
		vecLine = line.split()
		bins.append(vecLine[0])
		binsTemp.append(vecLine[1])
		
		for i in range(0,num_funcParams):
			funcParamLimits_dict[functionParameters[i]] = [vecLine[num_binParams*2 + 2*i +1],vecLine[num_binParams*2 + 2*i +2 ]]
		funcParamLimits_vec.append(funcParamLimits_dict)
		for i in range(0, num_tableFuncParams):
			tableFuncParams_temp.append(vecLine[num_allParams*2+1+i])
		tableFuncParams.append(tableFuncParams_temp)
bins.append(binsTemp[len(binsTemp)-1])


		
		
	
