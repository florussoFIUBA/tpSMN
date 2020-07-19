import pandas as pd
import matplotlib.pyplot as plt
import datetime

'''
Create dataFramework with the data from csv file (file)
'''
def CreateCsvDataFrame(file):
    df = pd.read_csv(file, index_col=False)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    return df

'''
Show average maximum and minimum yearly temperature values' plot of the
last (lastYears) years, from (lastYears) to (today) year, with
the dataFramework (df) information
'''
def CreateTemperaturesPlot(df, today, lastYears):
    yearList=[]
    maxTempList=[]
    minTempList=[]

    for i in range(lastYears, -1, -1):
        
        startDate=today.replace(year=today.year-i, month=1, day =1)
        finishDate=today.replace(year=today.year-i, month=12, day=31)
        yearList.append(startDate.year)
        maxTempList.append(df.loc[((df['Date']<=finishDate) & (df['Date']>=startDate)), 'Max Temperature'].mean())
        minTempList.append(df.loc[((df['Date']<=finishDate) & (df['Date']>=startDate)), 'Min Temperature'].mean())
       

    dfTempAvg=pd.DataFrame({'Temperatura Maxima':maxTempList, 'Temperatura Minima':minTempList}, index=yearList)
    

    temperaturePlot=dfTempAvg.plot.bar(title='Promedio de temperaturas anuales')
    temperaturePlot.set_xlabel("Año")
    temperaturePlot.set_ylabel("Promedio")
    plt.show()
    
   
'''
Show average yearly humidity values' plot of the last (lastYears) years, from (lastYears)
to (today) year, with the dataFramework (df) information
'''

def CreateHumidityPlot(df, today, lastYears):
    yearList=[]
    humidityList=[]
   
    for i in range(lastYears, -1, -1):
        
        startDate=today.replace(year=today.year-i, month=1, day =1)
        finishDate=today.replace(year=today.year-i, month=12, day=31)
        yearList.append(startDate.year)
        humidityList.append(df.loc[((df['Date']<=finishDate) & (df['Date']>=startDate)), 'Relative Humidity'].mean())
        

    dfHumAvg=pd.DataFrame({'Promedio humedad':humidityList}, index=yearList)
    

    humidityPlot=dfHumAvg.plot.bar(title='Promedio de humedad')
    humidityPlot.set_xlabel("Año")
    humidityPlot.set_ylabel("Promedio")
    plt.show()

'''
Show the maximum temperature value of the last (lastYears) years
'''
def getMaxTemperature(df, today, lastYears):
    
    startDate=today.replace(year=today.year-lastYears, month=1, day =1)
          
    return df.loc[((df['Date']<=today) & (df['Date']>=startDate)), 'Max Temperature'].max()
    
    

'''
Show the maximum humidity value of the last (lastYears) years
'''
def getMaxRainMm(df, today, lastYears):
    
    startDate=today.replace(year=today.year-lastYears, month=1, day =1)
    
    return df.loc[((df['Date']<=today) & (df['Date']>=startDate)), 'Precipitation'].max()
    

'''
Executions
'''
file='data.csv'
lastYears=7
today=(pd.to_datetime('today')).date()

df=CreateCsvDataFrame(file)
CreateTemperaturesPlot(df,today, lastYears)
CreateHumidityPlot(df,today, lastYears)
maxTemp=getMaxTemperature(df,today, lastYears)
maxRainMm=getMaxRainMm(df,today, lastYears)

print(maxTemp)
print(maxRainMm)