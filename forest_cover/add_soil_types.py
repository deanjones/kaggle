import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

def get_soil_type(x):
    for n in range(1,41):
        if x['Soil_Type' + str(n)]==1:
            return n

def get_tokens_for_soil_type(x, token_data):
    return token_data[x['Soil_Type']]

soil_types = pd.DataFrame.from_csv('soil_types.csv', sep='\t')

data = pd.read_table('scaled_test.csv', sep=',', index_col=False)

types = soil_types['SoilType']
type_values = types.to_dict().values()

stopwords = stopwords.words('english')
vectorizer = CountVectorizer(min_df=1, stop_words=stopwords)
fit = vectorizer.fit_transform(type_values)
token_data = pd.DataFrame.from_records(fit.toarray(), columns=vectorizer.get_feature_names(), index=range(1,41))

data['Soil_Type'] = data.apply(lambda x: get_soil_type(x), axis = 1)

data = data.merge(token_data, how='inner', left_on='Soil_Type', right_index=True)

data = data.drop('Soil_Type', 1)

print data.shape
data.to_csv('scaled_test2.csv', index=False)
