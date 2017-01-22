from requests import get, post
import json

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

def get_time(data):
    time = []
    items = data
    for item in items:
        time.append(item['Timestamp'])
    return time

def get_data(length=30, interval=5):
    '''
    :param length is the number of days of data we retrieve (int)
    :param interval is the number of minutes between each tick (int)
    :return {'Building_Name' : 
                {'Electricity' : [pts]
                 'Steam' : [pts]
                 'Chilled_Water': [pts]
                 }
              'Outside_Air_Temp':[{}]...
              'Time'
            }
    '''
    # https://bldg-pi-api.ou.ad3.ucdavis.edu/piwebapi/streams/P09KoOKByvc0-uxyvoTV1UfQViQAAAVVRJTC1QSS1QXEFSQ19TVEVBTV9ERU1BTkRfS0JUVQ/interpolated?startTime=*-30d&interval=1m

    # dummy data for now
    electricity_data = json.loads(open('/Users/jaclarke/Documents/HackDavis2017/app/tmp/12_23_1_21_1h_elec.json').read())['Items']
    steam_data = json.loads(open('/Users/jaclarke/Documents/HackDavis2017/app/tmp/12_23_1_21_1h_steam.json').read())['Items']
    # water_data = json.loads(open('/Users/jaclarke/Documents/HackDavis2017/app/tmp/12_23_1_21_1m_cwater.json').read())['Items']
    total_data = json.loads(open('/Users/jaclarke/Documents/HackDavis2017/app/tmp/12_23_1_21_1h_total.json').read())['Items']
    temp_data = json.loads(open('/Users/jaclarke/Documents/HackDavis2017/app/tmp/12_23_1_21_1h_airtemp.json').read())['Items']

    electricity_data_list = []
    steam_data_list = []
    total_data_list = []
    temp_data_list = []
    time_list = get_time(electricity_data)

    for i in range(len(electricity_data)):
        electricity_data_list.append(electricity_data[i]["Value"])
        steam_data_list.append(steam_data[i]["Value"])
        temp_data_list.append(temp_data[i]["Value"])
        total_data_list.append(total_data[i]["Value"])

    time = get_time(electricity_data)

    # we ensure all lists are the same size

    ret = {
        'Electricity' : electricity_data_list,
        'Steam' : steam_data_list,
        'Total' : total_data_list,
        'Temperature' : temp_data_list,
        'Time' : time_list
    }

    return ret

if __name__ == '__main__':
    get_data()