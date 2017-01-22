from datetime import datetime as dt

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

from math import floor

class Energy_Prediction_Model(object):
    '''
    Features:
    1. Weekday?
    2. What hour of the day?
    3. Air temperature
    '''
    def __init__(self, data_dict, train_partition):
        # initialize training and test data sets

        self.electricity_data = np.array(data_dict['Electricity'])
        self.electricity_train_data = np.array(self.electricity_data[:int(floor(len(self.electricity_data)*train_partition))])
        self.electricity_test_data = np.array(self.electricity_data[int(floor(len(self.electricity_data)*train_partition)):])

        self.steam_data = np.array(data_dict['Steam'])
        self.steam_train_data = np.array(self.steam_data[:int(floor(len(self.steam_data)*train_partition))])
        self.steam_test_data = np.array(self.steam_data[int(floor(len(self.steam_data)*train_partition)):])

        self.water_data = np.array(data_dict['Water'])
        self.water_train_data = np.array(self.water_data[:int(floor(len(self.water_data)*train_partition))])
        self.water_test_data = np.array(self.water_data[int(floor(len(self.water_data)*train_partition)):])

        self.air_temp = np.array(data_dict['Temperature'])
        self.air_temp_train_data = np.array(self.air_temp[:int(floor(len(self.air_temp)*train_partition))])
        self.air_temp_test_data = np.array(self.air_temp[int(floor(len(self.air_temp)*train_partition)):])

        self.time = np.array(data_dict['Time'])
        self.time_train_data = np.array(self.time[:int(floor(len(self.time)*train_partition))])
        self.time_test_data = np.array(self.time[int(floor(len(self.time)*train_partition)):])

        assert(len(self.electricity_data) == len(self.steam_data) == len(self.water_data) == len(self.air_temp) == len(self.time))

    def create_features(self, train_partition, avg_delta):

        features = []
        for i in range(len(self.time)):
            time = dt.strptime(self.time[i][:-3],  "%Y-%m-%dT%H:%M:%S.%f")
            is_weekday = 1 if time.isoweekday() in range(1,6) else 0
            hour = time.hour
            air_temp = self.air_temp[i]
            feature = [air_temp, is_weekday, hour]
            # for delta in deltas:
            if i >= 20:
                avg_temp = sum(self.air_temp[i-avg_delta:i]) / float(avg_delta)
                feature.append(avg_temp)
            else:
                avg_temp = sum(self.air_temp[:i]) / float(i+1)
                feature.append(avg_temp)
            features.append(feature)

        self.features_train_data = np.array(features[:int(floor(len(features)*train_partition))])
        self.features_test_data = np.array(features[int(floor(len(features)*train_partition)):])

    # we have individual functions so that I can refactor the NN architecture for each
    # prediction

    def train_electricity_model(self, loss, learning_rate=1, epochs=10, batch_size=200):
        assert(len(self.features_train_data) == len(self.electricity_train_data))

        # create model
        input_size = self.features_train_data.shape[1]
        electricity_model = Sequential()
        electricity_model.add(Dense(input_size, input_dim=input_size, init='normal', activation='relu'))
        electricity_model.add(Dense(1, init='normal'))
        electricity_model.compile(loss='mean_squared_error', optimizer='sgd')
        electricity_model.fit(self.features_train_data, self.electricity_train_data, nb_epoch = epochs, batch_size=batch_size)
        self.electricity_model = electricity_model

    def train_water_model(self, loss, learning_rate=10, epochs=10, batch_size=200):
        assert(len(self.features_train_data) == len(self.water_train_data))

        # create model
        input_size = self.features_train_data.shape[1]
        water_model = Sequential()
        water_model.add(Dense(input_size, input_dim=input_size, init='normal', activation='relu'))
        water_model.add(Dense(1, init='normal'))
        water_model.compile(loss='mean_squared_error', optimizer='sgd')
        water_model.fit(self.features_train_data, self.water_train_data, nb_epoch = epochs, batch_size=batch_size)
        self.water_model = water_model

    def train_steam_model(self, loss, learning_rate=0.001, epochs=10, batch_size=500):
        assert(len(self.features_train_data) == len(self.steam_train_data))

        # create model
        input_size = self.features_train_data.shape[1]
        steam_model = Sequential()
        steam_model.add(Dense(input_size, input_dim=input_size, init='normal', activation='relu'))
        steam_model.add(Dense(1, init='normal'))
        steam_model.compile(loss='mean_squared_error', optimizer='sgd')
        steam_model.fit(self.features_train_data, self.steam_train_data, nb_epoch = epochs, batch_size=batch_size)
        self.steam_model = steam_model

    def train(loss):
        

    def predict(self, x):

        # electricity_predictions = self.electricity_model.predict(self.electricity_test_data)
        # steam_predictions = self.steam_model.predict(self.steam_test_data)
        # water_predictions = self.water_model.predict(self.water_test_data)
        # print electricity_predictions, steam_predictions, water_predictions
        predictions = {
            'Electricity' : self.electricity_model.predict(x),
            'Steam' : self.steam_model.predict(x),
            'Water' : self.water_model.predict(x),
        }
        return predictions
