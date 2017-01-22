from flask_restful import Resource



class Energy_Prediction(Resource):

	# building_name_to_id = {
	#     'Ghau'
	# }

	def get(self, building_id):
		return 'hey'