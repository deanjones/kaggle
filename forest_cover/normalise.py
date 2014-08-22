import sys
import pandas as pd
import numpy as np
from sklearn import preprocessing
from add_soil_types import add_soil_types

def scale(unscaled_training_data, unscaled_test_data):
    scaler = preprocessing.MinMaxScaler()
    scaled_training_data = scaler.fit_transform(unscaled_training_data)
    scaled_test_data = scaler.transform(unscaled_test_data)
    return scaled_training_data, scaled_test_data

def encode_categorical_data(raw_data):
    cat_1 = 0.9
    cat_0 = 0.1
    # make sure we remove one column of each of the binary-coded features
    soil_cols = [u'Soil_Type' + unicode(n) for n in range(1, 40)]
    wilderness_cols = [u'Wilderness_Area' + unicode(n) for n in range(1, 4)]
    soil_cols.extend(wilderness_cols)
    binary_coded = pd.DataFrame(raw_data, columns=soil_cols)
    # standardise the binary-coded features
    binary_coded.replace(to_replace=0, value=cat_0, inplace=True)
    binary_coded.replace(to_replace=1, value=cat_1, inplace=True)
    return binary_coded

try:
    training_data_path = sys.argv[1]
    test_data_path = sys.argv[2]
except IndexError:
    print "Usage: normalise.py <training data> <test data>"
    quit()

raw_training_data = pd.DataFrame.from_csv(training_data_path)
raw_test_data = pd.DataFrame.from_csv(test_data_path)

columns_to_scale = ['Elevation', 
                    'Aspect', 
                    'Slope', 
                    'Horizontal_Distance_To_Hydrology', 
                    'Vertical_Distance_To_Hydrology', 
                    'Horizontal_Distance_To_Roadways', 
                    'Hillshade_9am', 
                    'Hillshade_Noon', 
                    'Hillshade_3pm', 
                    'Horizontal_Distance_To_Fire_Points']

training_data_to_scale = pd.DataFrame(raw_training_data, columns=columns_to_scale).astype(np.float64)
test_data_to_scale = pd.DataFrame(raw_test_data, columns=columns_to_scale).astype(np.float64)

scaled_training_data, scaled_test_data = scale(training_data_to_scale, test_data_to_scale)

scaled_training_data = pd.DataFrame(scaled_training_data, columns=columns_to_scale)
scaled_training_data = scaled_training_data.set_index(raw_training_data.index)

scaled_test_data = pd.DataFrame(scaled_test_data, columns=columns_to_scale)
scaled_test_data = scaled_test_data.set_index(raw_test_data.index)

binary_coded_training_data = encode_categorical_data(raw_training_data)
binary_coded_test_data = encode_categorical_data(raw_test_data)

# shift the cover_type to 0..6
shifted_cover_type = raw_training_data.Cover_Type - 1
scaled_training_data.insert(loc=0, column='Cover_Type', value=shifted_cover_type)
scaled_training_data['Cover_Type'] = scaled_training_data['Cover_Type'].astype(np.int32)

# merge the numerical and categorical data into a single data frame
all_training_data = scaled_training_data.merge(binary_coded_training_data, how='inner', left_index=True, right_index=True)

all_test_data = scaled_test_data.merge(binary_coded_test_data, how='inner', left_index=True, right_index=True)

print all_training_data.shape

all_training_data.to_csv('training_normalised.csv', index=False)
all_test_data.to_csv('test_normalised.csv', index=False)

# normalise the aspect to one-hot representation of E/N/W/S aspect
#northern_aspect_bool = (raw_data['Aspect'] < 90) | (raw_data['Aspect'] >= 270)
#northern_aspect = northern_aspect_bool.apply(lambda x: cat_1 if x==True else cat_0)
#southern_aspect_bool = (raw_data['Aspect'] >= 90) & (raw_data['Aspect'] < 270)
#southern_aspect = southern_aspect_bool.apply(lambda x: cat_1 if x==True else cat_0)
#western_aspect_bool = (raw_data['Aspect'] >= 180)
#western_aspect = western_aspect_bool.apply(lambda x: cat_1 if x==True else cat_0)
#eastern_aspect_bool = (raw_data['Aspect'] < 180)
#eastern_aspect = eastern_aspect_bool.apply(lambda x: cat_1 if x==True else cat_0)

