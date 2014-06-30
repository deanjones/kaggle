import pandas as pd
import random as rd

all_data = pd.read_table('scaled_data2.csv', sep=',', index_col=False)

n = 1000

valid_rows = rd.sample(all_data.index, n)

valid_data = all_data.ix[valid_rows]
train_data = all_data.drop(valid_rows)

valid_data.to_csv('valid_dataset.csv', index=False)
train_data.to_csv('train_dataset.csv', index=False)

