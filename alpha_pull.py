#!/anaconda3/bin/python
import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime 
from alpha_vantage.timeseries import TimeSeries
from alpha_key import key_def
 



def get_stock_close(comp, s1, s2):

  ALPHA_VANTAGE_API_KEY = key_def() 

  ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='integer')
  symb = 'NYSE:%(name)s' % dict(name=comp)
  print(symb)

  interday_data, meta_data = ts.get_daily_adjusted(symbol=symb, outputsize='full')

  # Print the information of the data
  alldatesstr = interday_data['index']
  alldates = []

  for idem in range(0,len(alldatesstr)):
      alldates.append(convert(alldatesstr[idem]))

  allclose = interday_data['4. close']
  #print(alldates)

  #print(alldates[1])
  #print(alldates[2])
  #print(alldates[3])

  date1 = convert(s1) 
  date2 = convert(s2) 

  date = []
  close = []


  for idam in range(0,len(alldates)):
    if ((alldates[idam]>=date1) and (alldates[idam]<=date2)):
      date.append(alldates[idam])
      close.append(allclose[idam])

  #print('The date of interest are ',date)

  with open('tesla_stock_try.csv', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(zip(date,close))

  return close

# converting time string to datetime format for comparison reasons
def convert(s):
  return datetime.strptime(s, '%Y-%m-%d')

if __name__ == '__main__':
  start = '2019-09-23'
  end = '2019-09-27'
  comp = 'TSLA'
  #print(convert(start))
  print(get_stock_close(comp,start,end))
