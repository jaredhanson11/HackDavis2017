from utils.model import Energy_Prediction_Model
from utils.data import *
import numpy as np

data_dict = get_data()

# print data_dict

model = Energy_Prediction_Model(data_dict, 0.70)
model.create_features(0.70, 20)
model.train_electricity_model('mean_squared_error')
model.train_steam_model('mean_squared_error')
model.train_water_model('mean_squared_error')
print model.predict(np.array([[45.,1,0,30.]]))