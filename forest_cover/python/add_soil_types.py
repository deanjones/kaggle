import sys
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

def get_soil_type(x):
    for n in range(1,41):
        if x['Soil_Type' + str(n)]==0.9:
            return n

def get_tokens_for_soil_type(x, token_data):
    return token_data[x['Soil_Type']]

def add_soil_types(data):
    soil_types = pd.DataFrame.from_csv('soil_types.csv', sep='\t')
    types = soil_types['SoilType']
    type_values = types.to_dict().values()

    sw = stopwords.words('english')
    vectorizer = CountVectorizer(min_df=1, stop_words=sw)
    fit = vectorizer.fit_transform(type_values)
    token_data = pd.DataFrame.from_records(fit.toarray(), columns=vectorizer.get_feature_names(), index=range(1, 41))
    token_data = token_data.applymap(lambda x: -1 if x==0 else 1)

    data['Soil_Type'] = data.apply(lambda x: get_soil_type(x), axis = 1)
    data = data.merge(token_data, how='inner', left_on='Soil_Type', right_index=True)

    data = data.drop('Soil_Type', 1)
    return data

try:
    input_path = sys.argv[1]
    out_path = sys.argv[2]
except IndexError:
    print "Usage: add_soil_types.py <input file> <output file>"
    quit()

input_data = pd.read_table(input_path, sep=',', index_col=False)
enhanced_data = add_soil_types(input_data)
enhanced_data.to_csv(out_path, index=False)
