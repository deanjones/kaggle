import sys
import pandas as pd
import random as rd

try:
    input_path = sys.argv[1]
    out_path1 = sys.argv[2]
    out_path2 = sys.argv[3]
    split_size = int(sys.argv[4])
except IndexError:
    print "Usage: split_data.py <input file> <output file1> <output file2> <size>"
    quit()

all_data = pd.read_table(input_path, sep=',', index_col=False)

valid_rows = rd.sample(all_data.index, split_size)

valid_data = all_data.ix[valid_rows]
train_data = all_data.drop(valid_rows)

valid_data.to_csv(out_path1, index=False)
train_data.to_csv(out_path2, index=False)

