#!/usr/bin/env python
"""

run the pipeline 

   (1) Associative stats
   (2) Predictive stats

"""


## make imports
import os,sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

sys.path.append(os.path.join("..","..","arvos"))
from Pipeline import Pipeline

results_dir = os.path.join(".","results")
pline = Pipeline(results_dir)

deseq_file = os.path.join(results_dir,"deseq.csv")
deseq_matrix_file = os.path.join(results_dir,"deseq-samples.csv")
targets_file = os.path.join(".","data","targets.csv")

X,y = pline.generate_features_and_targets(deseq_file,deseq_matrix_file,targets_file)


print("done")
sys.exit()




## init variables
fileIn = os.path.join('Advertising.csv')
project = "example"

## create a pandas data frame
data = pd.read_csv(fileIn, index_col=0)
print(data.head())
print("\ndata matrix: %s x %s"%(data.shape))

## visualize the relationship between the features and the response using scatterplots
features = ['TV','Radio','Newspaper']
response = ['Sales']

fig = plt.figure()
sns.pairplot(data, x_vars=features, y_vars=response, size=7, aspect=0.6, kind='reg')
plt.savefig("%s-scatter-pairs.png"%project)

## split data into training and testing
X = data[features]
y = data[response]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

## specify, fit and predict with model
linreg = LinearRegression()
linreg.fit(X_train, y_train)
y_pred = linreg.predict(X_test)

coefs = ";".join([str(round(c,3)) for c in linreg.coef_[0]])
print("intercept: %s"%(linreg.intercept_))
print("coefs")
for f,c in zip(features,coefs):
    print("\t%s,%s"%(f,c))

print("RMSE (%s): %s"%(";".join(features),np.sqrt(metrics.mean_squared_error(y_test,y_pred))))

## feature selection: does feature x improve our model in terms of RMSE
_features = ["TV","Radio"]
X = data[_features]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
linreg.fit(X_train, y_train)
y_pred = linreg.predict(X_test)
print("RMSE (%s): %s"%(";".join(_features),np.sqrt(metrics.mean_squared_error(y_test,y_pred))))


"""
We want to minimize error and because it went down we should remove the feature
"""
