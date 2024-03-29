# The Correlation of Twitter Sentiment with Stock Valuation
<img align="left" src=https://github.com/yerlansharipov/customer_consent/blob/master/pictures/market_summary.png width=400/>

## Can Twitter Help Investors Predict the Value of a Company’s Stock?


With Twitter users generating ample data during a day on multiple topics, the team  mines such data, with mentions of a specific company. The sentiment of these tweets is then correlated to the closing value of a stock by day. 
Shareholders and company executives may then be able to predict if dissatisfaction affects the value of their company and holdings

<br/><br/>
<br/><br/>
<br/><br/>


## The System Architecture
<img src=https://github.com/yerlansharipov/customer_consent/blob/master/pictures/system_architecture.png width=1200/>
<br/><br/>

## System Components
<img src=https://github.com/yerlansharipov/customer_consent/blob/master/pictures/system_components.png width=800/>
<br/><br/>

## How to Use
### Necessary Information:
- Company name and stock market abbreviation:
e.g. Tesla’s market abbreviation  TSLA
- Date range for needed analysis:
e.g. 2019-09-23 to 2019-09-27

### Necessary Programs:
Python

### Necessary Libraries:
Installable using pip:
tweepy
pandas
six
numpy
matplotlib
alpha-vantage
csv
google-cloud-language


## Sample output
<img src=https://github.com/yerlansharipov/customer_consent/blob/master/pictures/sample_output_graph.png width=400/>
<br/><br/>

## Lessons Learned
- Open-source API’s are tricky because there is no direct assistance from the API’s owners
- API’s are discontinued from time to time, e.g. the Yahoo Finance stock market API; and often, the data is limited, e.g. the Quandl stock market API provides data up to March 26, 2018
- There is a lot of potential with the Twitter API, aside from a sentiment analysis: the team can imagine extensive models which return most used words, heatmaps on where a product is used the most, etc. allowing entities such as small businesses or indie artists to thrive in the digital economy
- For some companies, there may not be a correlation between sentiment and stock value. For some, the correlation might be more visible over a long period of time. The correlation might even be mor elikely due to industry; perhaps, fashion might see higher correlation. The analysis can now be performed with the tool provided. 


