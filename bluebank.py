# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 16:57:48 2022

@author: Facu
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open('loan_data_json.json') as json_file:
    data = json.load(json_file)
    
loandata = pd.DataFrame(data)

#finding unique values for purpose column
loandata['purpose'].unique()

#describe the data
loandata.describe()

#describe the data for a specific column
loandata['int.rate'].describe()
loandata['fico'].describe()
loandata['dti'].describe()

#using EXP() func to get annual income
income = np.exp(loandata['log.annual.inc'])
loandata['annualincome'] = income

#using for loop on fico score
dfLength = len(loandata)
ficoScore = []

for x in range(0, dfLength):
    category = loandata['fico'][x]
    if category < 400:
        score = 'Poor'
    elif category >= 400 and category < 600:
        score = 'Fair'
    elif category >= 600 and category < 660:
        score = 'Good'
    elif category >= 660 and category < 700:
        score = 'Very good'
    elif category >= 700:
        score = 'Excellent'
    else:
        score = 'Uknown'
    ficoScore.append(score)
    
ficoScore = pd.Series(ficoScore)
loandata['fico.category'] = ficoScore


#for int.rate we create a new column that will tell us if is high or low using loc
loandata.loc[loandata['int.rate'] > 0.12, 'Int.Rate.Type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'Int.Rate.Type'] = 'Low'

#count number of loans for every category
categoryLoans = loandata.groupby(['fico.category']).size()
categoryLoans.plot.bar()
plt.show()

#scatter plots
ypoint = loandata['annualincome']
xpoint = loandata['dti']
plt.scatter(xpoint, ypoint)

#writting to a csv file
loandata.to_excel('loan_cleanned.xlsx', index = True)