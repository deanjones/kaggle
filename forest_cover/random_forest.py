from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import pandas as pd

data = pd.read_table('scaled_data2.csv', sep=',', index_col=False)
target = data.ix[:,0]
features = data.ix[:,1:]

clf = RandomForestClassifier(n_estimators = 50)
score = cross_validation.cross_val_score(clf, features, target, cv=10) 
print score.mean()
