import uproot, uproot_methods
import numpy as np

from numpy import sqrt,log,exp,abs
from numpy import maximum as max
from numpy import minimum as min
from numpy import power as pow

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
		tableFunctionParameters = [] # names of the table function parameters as they will be named in the function (p1,p2,p3)
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
		for i in range(num_tableFuncParams):
			tableFunctionParameters.append("p%i"%i)
		for n in range(1,num_binParams + 1):
			binParameters.append(params[n])
		for n in range(num_binParams +2,num_binParams+num_funcParams+2):
			functionParameters.append(params[n])
		allParams = functionParameters+tableFunctionParameters
		nParms      = 0
		while( function.count('[%i]'%nParms) ):
			function = function.replace('[%i]'%nParms,'p%i'%nParms)
			nParms += 1
		funcs_to_cap = ['max','exp','pow']
		for fun in funcs_to_cap:
			function = function.replace(fun,fun.upper())
		templatevars = ['x','y','z','w','t','s']
		for i in range(num_funcParams):
			function = function.replace(templatevars[i], functionParameters[i])
		for fun in funcs_to_cap:
			function = function.replace(fun.upper(),fun)
			strFunction = function
		# turn string function into lamda function 
		lstr = "lambda %s: %s" % (",".join(allParams), function)
		function = eval(lstr)
		# Function parameters limits dictionary
		funcParamLimits_dict = {}
		for i in functionParameters:
			funcParamLimits_dict[i] = np.empty([2,0])
		
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
					funcParamLimits_dict[functionParameters[i]]=np.append(funcParamLimits_dict[functionParameters[i]],[[float(vecLine[num_binParams*2 + 2*i +1])],[float(vecLine[num_binParams*2 + 2*i +2 ])]],axis=1)
				#funcParamLimits_vec.append(funcParamLimits_dict)
				for i in range(0, num_tableFuncParams):
					tableFuncParams_temp.append(vecLine[num_allParams*2+1+i])
				tableFuncParams.append(tableFuncParams_temp)
		bins.append(binsTemp[len(binsTemp)-1])
		
		
		
		
		self.num_binParams = num_binParams
		self.num_funcParams = num_funcParams
		self.binParameters  = binParameters   
		self.functionParameters = functionParameters
		self.bins           = np.array(bins)        
		self.funcParamLimits_dict   = funcParamLimits_dict
		self.tableFuncParams       = tableFuncParams
		self.tableFuncParamsNames = tableFunctionParameters
		self.allParams = allParams
		self.function=function
		self.strFunction = strFunction

	
	def evalIndex(self, binParam):
		
		bins = self.bins
		index = np.searchsorted(bins,binParam, side='right')-1
		
		return index
		
	def evalCorrections(self, *parameters):
		index = self.evalIndex(parameters[0])
		evalVars = []
		for n, var in enumerate(parameters):
			if n != 0:
				evalVars.append(np.maximum(parameters[n],self.funcParamLimits_dict[self.funcParamLimits_dict.keys()[n-1]][index]))
		return evalVars
			
		
	
