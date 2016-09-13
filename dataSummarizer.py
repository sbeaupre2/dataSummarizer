import os
import sys
import pandas as pd
import numpy as np
from collections import OrderedDict

def summarize(path,outputPath):
	fileList=list()
	for file in os.listdir(path):
		if file.endswith('.csv'):
			fileList.append(file)
	if len(fileList)<1:
		print('Nothing to summarize.')
	else:
		for file in fileList:
			fullInputFilePath=path+'/'+file
			inputDataFrame=pd.read_csv(fullInputFilePath)
			
			summaryData=dict() 
			# Not ordered dict because pandas sorts the row names in DataFrame.from_dict()

			#summaryData['File Name']=file
			#summaryData['Folder Name']=fullInputFilePath.split('/')[-2]
			#summaryData['Description']=""
			#summaryData['Number of Rows']=inputDataFrame.shape[0]
			#summaryData['Number of Columns']=inputDataFrame.shape[1]
			#columnNames=list(inputDataFrame)
			
			columnNames=inputDataFrame.columns.values.tolist()
			
			for column in columnNames:
				if inputDataFrame[column].dtype==np.float64 or \
				inputDataFrame[column].dtype==np.int64:
					columnType="Numeric"
				else:
					columnType="Non Numeric"
				
				allValues=inputDataFrame[column].ravel()
				NonNaValues = [x for x in allValues if str(x)!='nan']

				uniqueValues=set(NonNaValues)				
				uniqueCount=len(uniqueValues)
				validCount=len(NonNaValues)					
				naCount=len(allValues)-len(NonNaValues)

				sample=""
				i=0
				while len(uniqueValues)>0 and i<3:
					value=uniqueValues.pop()
					sample=sample+'('+str(value)+')'
					i=i+1
				
				rowDict=OrderedDict()
				rowDict['Description']=""
				rowDict['Type']=columnType
				rowDict['Valid Values']=validCount
				rowDict['Unique Values']=uniqueCount
				rowDict['NAs']=naCount
				rowDict['Sample Values']=sample
				rowDict['Comments']=""
				
				summaryData[column]=rowDict
	
				#summaryData[column]='Description:""'+';     '+\
				#'Type:'+columnType+';     '+\
				#'Total: '+str(validCount)+';     '+\
				#'Unique: '+str(uniqueCount)+';     '+\
				#'NA: '+str(naCount)+';     '+\
				#'Sample: '+sample+';     '+\
				#'Comments:"";'     
				 

			#print(summaryData)
			#for key in summaryData.keys():
			#	print(key)			
			#outputDataFrame=pd.DataFrame(list(summaryData.items()),
			#columns=['Field','Information'])
			#print(outputDataFrame.shape)
			#print(outputDataFrame)
			#print(summaryData.keys())
			#print(outputDataFrame.head())

			outputDataFrame=pd.DataFrame.from_dict(summaryData,orient='index')
			
			fullOutputFilePath=outputPath+'/'+file[0:-4]+'_Summary.csv'
			outputDataFrame.to_csv(fullOutputFilePath)

		print('\nSummarized '+str(len(fileList))+' file(s). Output at: '+outputPath+'.')
			
						

def main():
	
	if len(sys.argv)<3:
		print('The usage is "python3 dataSummarizer.py <input path> <output path>"\n'+
		'where <input path> contains the path to the directory to be examined and'+
		'<output path> contains the path to the directory where the summaries are to be stored.')
	else:		
		path=sys.argv[1]
		outputPath=sys.argv[2]
		os.makedirs(outputPath, exist_ok=True)
		summarize(path,outputPath)
	

if __name__=='__main__':
	main()


	
