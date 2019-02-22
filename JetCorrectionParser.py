import uproot, uproot_methods
import numpy as np

filePath = "files/test.txt"
f = open(filePath, 'r').readlines()
'''
This script parses a Jet correction txt file and stores its components in arrays.
It creates the following variables:

1) binParameters     list with the names of the variables that are expected to perform the lookup
2) functionParameters    list with the names of the variables that are expected to evaluate the function
3) bins              list with the binnig of the binParameters  * currently only for 1D, one binParameter
4) funcParamLimits_vec    a vector containing dictionaries each with the the upper an lower limits of the function parameters 
5) tableFuncParams        a vector containing the table function parameters 


'''
class CorrectionParser(object):
	
	def __init__ (self, file_path):
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
				bins.append(float(vecLine[0]))
				binsTemp.append(float(vecLine[1]))
				
				for i in range(0,num_funcParams):
					funcParamLimits_dict[functionParameters[i]] = [vecLine[num_binParams*2 + 2*i +1],vecLine[num_binParams*2 + 2*i +2 ]]
				funcParamLimits_vec.append(funcParamLimits_dict)
				for i in range(0, num_tableFuncParams):
					tableFuncParams_temp.append(vecLine[num_allParams*2+1+i])
				tableFuncParams.append(tableFuncParams_temp)
		bins.append(binsTemp[len(binsTemp)-1])
		self.binParameters  = binParameters   
		self.functionParameters = functionParameters
		self.bins           = np.array(bins)        
		self.funcParamLimits_vec   = funcParamLimits_vec 
		self.tableFuncParams       = tableFuncParams

	def evalIndex(self, binParam,):
		
		bins = self.bins
		index = np.searchsorted(bins,binParam, side='right')-1
		return index
		
		
	
