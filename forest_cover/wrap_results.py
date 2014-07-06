import pandas as pd
import sys

try:
    input_path = sys.argv[1]
    out_path = sys.argv[2]
except IndexError:
    print "Usage: wrap_results.py <input file> <output file>"
    quit()

with open(input_path, 'r') as f:
    result_list = [int(line.rstrip('\n')) + 1 for line in f]

result_data = {'Id': range(15121, 15121 + len(result_list)), 'Cover_Type': result_list}

df = pd.DataFrame(result_data)

df.to_csv(out_path, cols=['Id', 'Cover_Type'], index=False)
