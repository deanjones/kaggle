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

# re-scale the elevation to range -1..1
elev_float = raw_data['Elevation'].values.astype(np.float64)
scaled_elevation = preprocessing.scale(elev_float)

aspect_float = raw_data['Aspect'].values.astype(np.float64)
scaled_aspect = preprocessing.scale(elev_float)

# normalise the aspect to one-hot representation of E/N/W/S aspect
northern_aspect_bool = (raw_data['Aspect'] < 90) | (raw_data['Aspect'] >= 270)
northern_aspect = northern_aspect_bool.apply(lambda x: 1 if x==True else -1)
southern_aspect_bool = (raw_data['Aspect'] >= 90) & (raw_data['Aspect'] < 270)
southern_aspect = southern_aspect_bool.apply(lambda x: 1 if x==True else -1)
western_aspect_bool = (raw_data['Aspect'] >= 180)
western_aspect = western_aspect_bool.apply(lambda x: 1 if x==True else -1)
eastern_aspect_bool = (raw_data['Aspect'] < 180)
eastern_aspect = eastern_aspect_bool.apply(lambda x: 1 if x==True else -1)

# normalise slope to range 0..1
slope_float = raw_data['Slope'].values.astype(np.float64)
scaled_slope = preprocessing.scale(slope_float)

# normalise horizontal distance / vertical distance to hydrology 
# to distance to hydrology in range 0..1

hdth_float = raw_data['Horizontal_Distance_To_Hydrology'].values.astype(np.float64)
scaled_hdth = preprocessing.scale(hdth_float)

vdth_float = raw_data['Vertical_Distance_To_Hydrology'].values.astype(np.float64)
scaled_vdth = preprocessing.scale(vdth_float)

hdtr_float = raw_data['Horizontal_Distance_To_Roadways'].values.astype(np.float64)
scaled_hdtr = preprocessing.scale(hdtr_float)

hdtfp_float = raw_data['Horizontal_Distance_To_Fire_Points'].values.astype(np.float64)
scaled_hdtfp = preprocessing.scale(hdtr_float)

hillshade_noon_float = raw_data.Hillshade_Noon.values.astype(np.float64)
scaled_hillshade_noon = preprocessing.scale(hillshade_noon_float)

hillshade_9am_float = raw_data.Hillshade_9am.values.astype(np.float64)
scaled_hillshade_9am = preprocessing.scale(hillshade_noon_float)

hillshade_3pm_float = raw_data.Hillshade_3pm.values.astype(np.float64)
scaled_hillshade_3pm = preprocessing.scale(hillshade_noon_float)

if 'Cover_Type' in raw_data.columns:
    items = [('Cover_Type', raw_data.Cover_Type)]
else:
    items = []

items.extend([('Elevation', scaled_elevation),
#              ('Aspect', scaled_aspect),
             ('Northern_Aspect', northern_aspect),
             ('Eastern_Aspect', eastern_aspect),
             ('Southern_Aspect', southern_aspect),
             ('Western_Aspect', western_aspect),
             ('Slope', scaled_slope),
             ('Horizontal_Distance_To_Hydrology', scaled_hdth),
             ('Vertical_Distance_To_Hydrology', scaled_vdth),
             ('Horizontal_Distance_To_Roadways', scaled_hdtr),
             ('Hillshade_9am', scaled_hillshade_9am),
             ('Hillshade_Noon', scaled_hillshade_noon),
             ('Hillshade_3pm', scaled_hillshade_3pm),
             ('Horizontal_Distance_To_Fire_Points', scaled_hdtfp)])

# assemble into a data frame
scaled_data = pd.DataFrame.from_items(items)
scaled_data = scaled_data.set_index(raw_data.index)

# remove one column of each of the binary-coded features
soil_cols = [u'Soil_Type' + unicode(n) for n in range(1, 40)]
wilderness_cols = [u'Wilderness_Area' + unicode(n) for n in range(1, 4)]

soil_cols.extend(wilderness_cols)

binary_coded = pd.DataFrame(raw_data, columns=soil_cols)

# standard the binary-coded features to (1, -1)
binary_coded.replace(to_replace=0, value=-1, inplace=True)

all_data = scaled_data.merge(binary_coded, how='inner', left_index=True, right_index=True)

print all_data.shape

all_data.to_csv(out_path, index=False)
