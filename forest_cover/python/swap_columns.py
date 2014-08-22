import sys
import pandas as pd
import numpy as np
from sklearn import preprocessing

try:
    input_path = sys.argv[1]
    out_path = sys.argv[2]
except IndexError:
    print "Usage: normalise.py <input file> <output file>"
    quit()

data = pd.DataFrame.from_csv(input_path, header=0)

cols = data.columns.tolist()
cols = cols[-1:] + cols[:-1]
data = data[cols]

data.to_csv(out_path, index=False)
