#!/anaconda3/bin/python
import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime 
# Import TimeSeries class
from alpha_vantage.timeseries import TimeSeries
from alpha_key import key_def
 
ALPHA_VANTAGE_API_KEY = key_def() 
 

ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='integer')
 

interday_data, meta_data = ts.get_daily_adjusted(symbol='NYSE:TSLA', outputsize='full')

# Print the information of the data
alldatesstr = interday_data['index']
alldates = []

def convert(s):
  return datetime.strptime(s, '%Y-%m-%d')
for idem in range(0,len(alldatesstr)):
    #datetime.strptime('alldatesstr[idem]' , '%Y-%m-%d')
  alldates.append(convert(alldatesstr[idem]))

allclose = interday_data['4. close']
#print(alldates)

print(alldates[1])
date1 = datetime(2019, 9, 16) 
date2 = datetime(2019, 9, 20) 

date = []
close = []


for idam in range(0,len(alldates)):
  if ((alldates[idam]>=date1) and (alldates[idam]<=date2)):
    date.append(alldates[idam])
    close.append(allclose[idam])

print('The date of interest are ',date)

with open('tesla_stock_try.csv', 'w') as f:
  writer = csv.writer(f, delimiter='\t')
  writer.writerows(zip(date,close))