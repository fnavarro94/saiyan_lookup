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
function = params[2+num_funcParams+num_binParams]

for n in range(1,num_binParams + 1):
	binParameters.append(params[n])
for n in range(num_binParams +2,num_binParams+num_funcParams+2):
	functionParameters.append(params[n])

for n, line in enumerate(f):
	if n==0 or line=='\n':
		continue
	else:
		print n
		vecLine = line.split()
		bins.append(vecLine[0])
		binsTemp.append(vecLine[1])
		
bins.append(binsTemp[len(binsTemp)-1])


		
		
	
