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

raw_data = pd.DataFrame.from_csv(input_path)

# normalise the aspect to one-hot representation of E/N/W/S aspect
northern_aspect_bool = (raw_data['Aspect'] < 45) | (raw_data['Aspect'] >= 315)
northern_aspect = northern_aspect_bool.apply(lambda x: 1 if x==True else 0)
eastern_aspect_bool = (raw_data['Aspect'] >= 45) & (raw_data['Aspect'] < 135)
eastern_aspect = eastern_aspect_bool.apply(lambda x: 1 if x==True else 0)
southern_aspect_bool = (raw_data['Aspect'] >= 135) & (raw_data['Aspect'] < 225)
southern_aspect = southern_aspect_bool.apply(lambda x: 1 if x==True else 0)
western_aspect_bool = (raw_data['Aspect'] >= 225) & (raw_data['Aspect'] < 315)
western_aspect = western_aspect_bool.apply(lambda x: 1 if x==True else 0)

if 'Cover_Type' in raw_data.columns:
    items = [('Cover_Type', raw_data.Cover_Type)]
else:
    items = []

items.extend([('Elevation', raw_data.Elevation),
#              ('Aspect', scaled_aspect),
             ('Northern_Aspect', northern_aspect),
             ('Eastern_Aspect', eastern_aspect),
             ('Southern_Aspect', southern_aspect),
             ('Western_Aspect', western_aspect),
             ('Slope', raw_data.Slope),
             ('Horizontal_Distance_To_Hydrology', raw_data.Horizontal_Distance_To_Hydrology),
             ('Vertical_Distance_To_Hydrology', raw_data.Vertical_Distance_To_Hydrology),
              ('Horizontal_Distance_To_Roadways', raw_data.Horizontal_Distance_To_Roadways),
#             ('Hillshade_9am', scaled_hillshade_9am),
#             ('Hillshade_Noon', scaled_hillshade_noon),
#             ('Hillshade_3pm', scaled_hillshade_3pm),
              ('Horizontal_Distance_To_Fire_Points', raw_data.Horizontal_Distance_To_Fire_Points)])

# assemble into a data frame
scaled_data = pd.DataFrame.from_items(items)
scaled_data = scaled_data.set_index(raw_data.index)
soil_cols = [u'Soil_Type' + unicode(n) for n in range(1, 41)]
wilderness_cols = [u'Wilderness_Area' + unicode(n) for n in range(1,5)]
soil_cols.extend(wilderness_cols)
missing_data = pd.DataFrame(raw_data, columns=soil_cols)

all_data = scaled_data.merge(missing_data, how='inner', left_index=True, right_index=True)

all_data.to_csv(out_path, index=False)
