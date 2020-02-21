import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing

df=pd.read_csv('export.csv', sep=',',header=None)
targetvec = df[0]
le = preprocessing.LabelEncoder()
targets = le.fit_transform(targetvec)
#delete targets
features = df
features = features.drop(0, axis=1)
# delete last col
features = features.drop(87, axis=1)
#print(targets)
#print(features)

clf = RandomForestClassifier(n_estimators=20, max_depth=2, random_state=0)
#clf = DecisionTreeClassifier(random_state=0)
clf.fit(features, targets)
print(clf.feature_importances_)

preds=pd.read_csv('predictions.csv', sep=',',header=None)
preds = preds.drop(86, axis=1)
res = clf.predict(preds)
res = le.inverse_transform(res)
print(res)