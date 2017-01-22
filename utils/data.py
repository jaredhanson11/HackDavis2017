from requests import get, post

STREAM_BASE_URL = 'https://bldg-pi-api.ou.ad3.ucdavis.edu/piwebapi/streams/'

SOURCES = ['Ghausi']

def get_web_ids(source):
    CHILLED_WATER_TOKEN = 'ChilledWater_Demand_kBtu'
    ELECTRICITY_TOKEN = 'Electricity_Demand_kBtu'
    STEAM_TOKEN = 'Steam_Demand_kBtu'
    '''
    :param source to search for the relavant webids that identify the building and energy type
    :return {'Electricity': webid, ...}
    '''
    # https://bldg-pi-api.ou.ad3.ucdavis.edu/piwebapi/search/query?q=*Ghausi*demand_kbtu*
    return True

def get_data(length=30, interval=1)
    '''
    :param length is the number of days of data we retrieve (int)
    :param interval is the number of minutes between each tick (int)
    :return {'Building_Name' : 
                {'Electricity' : [pts]
                 'Steam' : [pts]
                 'Chilled_Water': [pts]
                 }
              'Outside_Air_Temp':[{}]...
            }
    '''
    # https://bldg-pi-api.ou.ad3.ucdavis.edu/piwebapi/streams/P09KoOKByvc0-uxyvoTV1UfQViQAAAVVRJTC1QSS1QXEFSQ19TVEVBTV9ERU1BTkRfS0JUVQ/interpolated?startTime=*-30d&interval=1m
    return True

def downsample(data_dict, interval=1):
    '''
    :param data_dict {'Building_Name' : {'elec' : [{}...]
    :param interval the number of hours to downsample to
    '''
    STOP = int(math.floor(interval * 60))
    outside_air_temp = data_dict['Outside_Air_Temperature']
    for building in data_dict:
        data = data_dict[building]
        electricity_data = data['Electricity']
        steam_data = data['Steam']
        chilled_water_data = data['Chilled_Water']
        length = len(chilled_water_data)
        electricity_data_ds = []

        for i in range(length):

        while count < 60:

