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

        self.total_data = np.array(data_dict['Total'])
        self.total_train_data = np.array(self.total_data[:int(floor(len(self.total_data)*train_partition))])
        self.total_test_data = np.array(self.total_data[int(floor(len(self.total_data)*train_partition)):])

        self.air_temp = np.array(data_dict['Temperature'])
        self.air_temp_train_data = np.array(self.air_temp[:int(floor(len(self.air_temp)*train_partition))])
        self.air_temp_test_data = np.array(self.air_temp[int(floor(len(self.air_temp)*train_partition)):])

        self.time = np.array(data_dict['Time'])
        self.time_train_data = np.array(self.time[:int(floor(len(self.time)*train_partition))])
        self.time_test_data = np.array(self.time[int(floor(len(self.time)*train_partition)):])

        assert(len(self.electricity_data) == len(self.steam_data) == len(self.total_data) == len(self.air_temp) == len(self.time))

    def create_features(self, train_partition, avg_delta):

        features = []
        for i in range(len(self.time)):
            time = dt.strptime(self.time[i][:-3],  "%Y-%m-%dT%H:%M:%S.%f")
            is_weekday = 1 if time.isoweekday() in range(1,6) else 0
            hour = time.hour
            air_temp = self.air_temp[i]
            feature = [air_temp, is_weekday, hour]
            features.append(feature)

        self.features_train_data = np.array(features[:int(floor(len(features)*train_partition))])
        self.features_test_data = np.array(features[int(floor(len(features)*train_partition)):])

    # we have individual functions so that I can refactor the NN architecture for each
    # prediction

    def train_electricity_model(self, loss, learning_rate=0.01, epochs=50, batch_size=256):
        assert(len(self.features_train_data) == len(self.electricity_train_data))

        # create model
        input_size = self.features_train_data.shape[1]
        electricity_model = Sequential()
        electricity_model.add(Dense(input_size, input_dim=input_size, activation='relu'))
        electricity_model.add(Dense(input_size, input_dim=input_size, activation='relu'))
        electricity_model.add(Dense(1, init='normal'))
        electricity_model.compile(loss='mean_squared_error', optimizer='sgd')
        electricity_model.fit(self.features_train_data, self.electricity_train_data, nb_epoch = epochs, batch_size=batch_size)
        self.electricity_model = electricity_model

    def train_total_model(self, loss, learning_rate=0.01, epochs=50, batch_size=256):
        assert(len(self.features_train_data) == len(self.total_train_data))

        # create model
        input_size = self.features_train_data.shape[1]
        total_model = Sequential()
        total_model.add(Dense(input_size, input_dim=input_size, activation='relu'))
        total_model.add(Dense(input_size, input_dim=input_size, activation='relu'))
        total_model.add(Dense(1, init='normal'))
        total_model.compile(loss='mean_squared_error', optimizer='sgd')
        total_model.fit(self.features_train_data, self.total_train_data, nb_epoch = epochs, batch_size=batch_size)
        self.total_model = total_model

    def train_steam_model(self, loss, learning_rate=0.01, epochs=50, batch_size=256):
        assert(len(self.features_train_data) == len(self.steam_train_data))

        # create model
        input_size = self.features_train_data.shape[1]
        steam_model = Sequential()
        steam_model.add(Dense(input_size, input_dim=input_size, activation='relu'))
        steam_model.add(Dense(input_size, input_dim=input_size, activation='relu'))
        steam_model.add(Dense(1, init='normal'))
        steam_model.compile(loss='mean_squared_error', optimizer='sgd')
        steam_model.fit(self.features_train_data, self.steam_train_data, nb_epoch = epochs, batch_size=batch_size)
        self.steam_model = steam_model     

    def evaluate(self):
        print '------'
        print self.electricity_model.evaluate(self.features_test_data, self.electricity_test_data)
        print self.steam_model.evaluate(self.features_test_data, self.steam_test_data)
        print self.total_model.evaluate(self.features_test_data, self.total_test_data)

    def predict(self, x):

        elec, steam, total = self.electricity_model.predict(x), self.steam_model.predict(x), self.total_model.predict(x)
        predictions = {
            'Electricity' : elec,
            'Steam' : steam,
            'Total' : total,
            'Water' : total-steam-elec
        }
        return predictions
