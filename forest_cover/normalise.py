import pandas as pd
import numpy as np
from sklearn import preprocessing

raw_data = pd.DataFrame.from_csv('test.csv')

# re-scale the elevation to range -1..1
elev_float = raw_data['Elevation'].values.astype(np.float64)
scaled_elevation = preprocessing.scale(elev_float)

# normalise the aspect to one-hot representation of E/N/W/S aspect
northern_aspect_bool = (raw_data['Aspect'] < 45) | (raw_data['Aspect'] >= 315)
northern_aspect = northern_aspect_bool.apply(lambda x: 1 if x==True else 0)
eastern_aspect_bool = (raw_data['Aspect'] >= 45) & (raw_data['Aspect'] < 135)
eastern_aspect = eastern_aspect_bool.apply(lambda x: 1 if x==True else 0)
southern_aspect_bool = (raw_data['Aspect'] >= 135) & (raw_data['Aspect'] < 225)
southern_aspect = southern_aspect_bool.apply(lambda x: 1 if x==True else 0)
western_aspect_bool = (raw_data['Aspect'] >= 225) & (raw_data['Aspect'] < 315)
western_aspect = western_aspect_bool.apply(lambda x: 1 if x==True else 0)

# normalise slope to range 0..1
slope_float = raw_data['Slope'].values.astype(np.float64)
scaled_slope = preprocessing.scale(slope_float)

# normalise horizontal distance / vertical distance to hydrology 
# to distance to hydrology in range 0..1
distance_to_hydrology = ((raw_data['Horizontal_Distance_To_Hydrology'] ** 2) + (raw_data['Vertical_Distance_To_Hydrology'] ** 2)) ** 0.5
scaled_distance_to_hydrology = preprocessing.scale(distance_to_hydrology)

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

# assemble into a data frame
scaled_data = pd.DataFrame({
                            'Elevation' : scaled_elevation,
                            'Northern_Aspect' : northern_aspect,
                            'Eastern_Aspect' : eastern_aspect,
                            'Southern_Aspect' : southern_aspect,
                            'Western_Aspect' : western_aspect,
                            'Slope': scaled_slope,
                            'Distance_To_Hydrology': scaled_distance_to_hydrology,
                            'Horizontal_Distance_To_Hydrology': scaled_hdth, 
                            'Vertical_Distance_To_Hydrology': scaled_vdth,
                            'Horizontal_Distance_To_Fire_Points': scaled_hdtfp,
                            'Hillshade_9am': scaled_hillshade_9am,
                            'Hillshade_Noon': scaled_hillshade_noon,
                            'Hillshade_3pm': scaled_hillshade_3pm})

soil_cols = [u'Soil_Type' + unicode(n) for n in range(1, 41)]
wilderness_cols = [u'Wilderness_Area' + unicode(n) for n in range(1,5)]
soil_cols.extend(wilderness_cols)
missing_data = pd.DataFrame(raw_data, columns=soil_cols)

all_data = scaled_data.merge(missing_data, how='inner', left_index=True, right_index=True)
all_data.to_csv('scaled_test.csv', index=False)
