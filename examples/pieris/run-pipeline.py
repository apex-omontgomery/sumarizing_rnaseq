#!/usr/bin/env python
"""

run the pipeline

   (1) Associative stats
   (2) Predictive stats

"""


## make imports
import os,sys,ast,csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics, svm

sys.path.append(os.path.join("..","..","arvos"))
from Pipeline import Pipeline

results_dir = os.path.join(".","results")
pline = Pipeline(results_dir)

deseq_file = os.path.join(results_dir,"deseq.csv")
deseq_matrix_file = os.path.join(results_dir,"deseq-samples.csv")
targets_file = os.path.join(".","data","targets.csv")

X,y = pline.generate_features_and_targets(deseq_file,deseq_matrix_file,targets_file)


## use saved grid search parameters
log_file = "estimated-params.log"
if not os.path.exists(log_file):
    print("training data has been saved.  Run grid_search.py then run this function again")
    sys.exit()

print("loading saved parameters...")
with open(log_file, 'r') as fid:
    reader = csv.reader(fid)
    params = {key: ast.literal_eval(value) for (key,value) in reader}


#### Run the classifiers ####
print("...running cross validated model(s)")

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)


## run a svm alone
print("...running svm")
clf_svm = svm.SVC(probability=True,
                  kernel=params['svm']['kernel'],
                  C=params['svm']['C'],
                  gamma=params['svm']['gamma'])
y_score_svm = clf_svm.fit(X, y).decision_function(X)

## run a random forest



## plot roc curves




# Compute micro-average ROC curve and ROC area
fpr, tpr, _ = metrics.roc_curve(y, y_score_svm)
roc_auc = metrics.auc(fpr, tpr)

'''
plt.figure()
'''
print("Done")
sys.exit()
