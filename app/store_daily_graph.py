from utils.model import Energy_Prediction_Model
from datetime import datetime
from requests import get
import numpy as np
import json

building_list = [
    {
        'building_name': 'Ghausi Hall',
        'building_id': 1,
        'electric_id': 'P09KoOKByvc0-uxyvoTV1UfQlhkAAAVVRJTC1QSS1QXEdIQVVTSV9FTEVDVFJJQ0lUWV9ERU1BTkRfS1c',
        'steam_id': 'P09KoOKByvc0-uxyvoTV1UfQ2CMAAAVVRJTC1QSS1QXEdIQVVTSV9TVEVBTV9ERU1BTkRfS0JUVQ',
        'total_id': 'P09KoOKByvc0-uxyvoTV1UfQxCMAAAVVRJTC1QSS1QXEdIQVVTSV9UT1RBTF9ERU1BTkQ',
        'temperature_id': 'A0EbgZy4oKQ9kiBiZJTW7eugwvuNJoeTC5hGUXQAVXTB8PAWy7CAixhtkadNNHmtOUXxgVVRJTC1BRlxDRUZTXFVDREFWSVNcV0VBVEhFUnxPVVRTSURFIEFJUiBURU1Q'
    },
    {
        'building_name': 'Chemistry Annex',
        'building_id': 2,
        'electric_id': 'P09KoOKByvc0-uxyvoTV1UfQlhkAAAVVRJTC1QSS1QXEdIQVVTSV9FTEVDVFJJQ0lUWV9ERU1BTkRfS1c',
        'steam_id': 'P09KoOKByvc0-uxyvoTV1UfQ2CMAAAVVRJTC1QSS1QXEdIQVVTSV9TVEVBTV9ERU1BTkRfS0JUVQ',
        'total_id': 'P09KoOKByvc0-uxyvoTV1UfQxCMAAAVVRJTC1QSS1QXEdIQVVTSV9UT1RBTF9ERU1BTkQ',
        'temperature_id': 'A0EbgZy4oKQ9kiBiZJTW7eugwvuNJoeTC5hGUXQAVXTB8PAWy7CAixhtkadNNHmtOUXxgVVRJTC1BRlxDRUZTXFVDREFWSVNcV0VBVEhFUnxPVVRTSURFIEFJUiBURU1Q'
    }
]




def get_forecast(lat, lon):
    base_url ='https://api.darksky.net/forecast/dd61ffb92f66ab0feee2573757eeddb3/'
    query = base_url + str(lat) + ',' + str(lon)
    r = get(query).json()['hourly']['data']
    data = map(lambda curr: {'time': curr['time'], 'temperature': curr['temperature']}, r)
    return data

def forcast_to_features(forecast):
    data_array = []
    for fc in forecast:
        dt = datetime.fromtimestamp(fc['time'])
        temp = fc['temperature']
        temp_feature = int(temp)
        if dt.weekday() in [5,6]:
            is_weekday = 0
        else:
            is_weekday = 1
        data = [temp_feature, dt.hour, is_weekday]
        data_array.append(data)


forecast = get_forecast()
prediction_data = forcast_to_features(forecast)

for building_obj in building_list:
    data_dict = get_data(building_obj)
    model = Energy_Prediction_Model(data_dict, 0.70)
    model.create_features(0.70, 20)
    model.train_electricity_model('mean_squared_error')
    model.train_steam_model('mean_squared_error')
    model.train_total_model('mean_squared_error')
    prediction = model.predict(prediction_data)
    saved_json = {'forecast': forecast, 'predictions': prediction}
    json.dump(saved_js, open('/static/data/' + buildinObj['building_id'] + '.json'))
