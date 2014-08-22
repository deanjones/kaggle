import sys
import pandas as pd
import random as rd

try:
    input_path = sys.argv[1]
    train_path = sys.argv[2]
    valid_path = sys.argv[3]
    test_path = sys.argv[4]
    split_size = int(sys.argv[5])
except IndexError:
    print "Usage: split_data.py <input file> <train file> <valid file> <test file> <size>"
    quit()

all_data = pd.read_table(input_path, sep=',', index_col=False)

test_and_valid_rows = rd.sample(all_data.index, split_size * 2)
#valid_rows = rd.sample(all_data.index, split_size)

valid_data = all_data.ix[test_and_valid_rows[0:split_size]]
test_data = all_data.ix[test_and_valid_rows[split_size:split_size*2]]
train_data = all_data.drop(test_and_valid_rows)
#train_data = all_data.drop(valid_rows)

valid_data.to_csv(valid_path, index=False)
test_data.to_csv(test_path, index=False)
train_data.to_csv(train_path, index=False)

