import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import pandas as pd

try:
    data = sys.argv[1]
except IndexError:
    print "Usage: random_forest.py <data>"
    quit()

data = pd.read_table(data, sep=',', index_col=False)
target = data.ix[:,0]
features = data.ix[:,1:]

clf = RandomForestClassifier(n_estimators = 50)
score = cross_validation.cross_val_score(clf, features, target, cv=10) 
print score.mean()
