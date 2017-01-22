from . import api
from controllers import Energy_Prediction

def add_resources():
    api.add_resource(Energy_Prediction.Energy_Prediction, '/buildings/<int:building_id>')