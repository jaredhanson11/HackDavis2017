import pandas as pd 
from sklearn.linear_model import Ridge, Lasso
from math import floor
import matplotlib.pyplot as plt
import numpy as np
from utils import plot
from copy import deepcopy
import sys
import pickle

def get_features_targets(length, delta, data=data):

	"""
	sandbox for iterating through different feature combinations
	length and delta can be arrays so that multiple predictions can be made Y^(x1, x2) = (h(x1),g(x2))
	where and g are trained separately
	:param data: a pandas DataFrame of daily data for fname
	:param length: the number of days of features
	:param length: the difference in days between the feature series and the target value
	:return (x,y): the x features and y targets
	"""

	assert delta > 0 and length > 0

	data_rows = data.values.tolist()
	x, y, = [], []

	# create x feature vectors
	for i in range(delta-1, len(data_rows)-length):

		tmp = data_rows[i:i+length]
		
		close = [z[1] for z in tmp]
		vol = [z[2] for z in tmp]
		op = [z[3] for z in tmp]
		hi = [z[4] for z in tmp]
		lo = [z[5] for z in tmp]
		drep = close + vol + op + hi + lo

		x.append(drep)

		# append next 
		y.append(data_rows[i-delta+1][1])

	return (x,y)

# idea: predict price using 30, 60, 90 days of data. then em on these values to determine the 
# linear interpolation coefficients

reg = np.linspace(1e-3,1e3,100)

def linear_model(x,y,reg_type,val_stat,partition,max_iter):
	"""
	:param x: x features
	:param y: y targets
	:param type: 'lasso' or 'ridge' regression
	:param val_stat: 'rsquared' or ...
	:param partition: a tuple of partitions for training, validation, and test data e.g. (.70,.20,.10)
	:return model: model with optimal regularization, validated with holdout set
	"""
	assert reg_type == 'ridge' or reg_type == 'lasso'
	assert val_stat == 'rsquared' # for now

	train_p, val_p, test_p = partition
	train_x, train_y = x[:int(floor(len(x)*train_p))], y[:int(floor(len(y)*train_p))]
	val_x, val_y = x[int(floor(len(x)*train_p)):int(floor(len(x)*(train_p+val_p)))], \
	y[int(floor(len(y)*train_p)):int(floor(len(y)*(train_p+val_p)))]
	test_x, test_y = x[int(floor(len(x)*(train_p+val_p))):], y[int(floor(len(y)*(train_p+val_p))):]

	model = None
	if reg_type == 'ridge':
		model = Ridge(fit_intercept=True, max_iter=max_iter)
	elif reg_type == 'lasso':
		model = Lasso(fit_intercept=True, max_iter=max_iter)

	optimal_model = model
	max_score = 0

	# iterate through the set of regularizations
	for r in reg:
		model.alpha = r
		model.fit(train_x,train_y)
		tmp = model.score(val_x,val_y)
		if tmp > max_score:
			optimal_model = deepcopy(model)
			max_score = tmp

	pred_x = range(len(test_x))
	pred_y = optimal_model.predict(test_x)
	plt.plot(pred_x,pred_y, '-r', label='Prediction')
	plt.plot(pred_x, test_y, '-b', label='Actual')
	plt.legend(loc='upper left')
	plt.show()

        # direction prediction
        denom = len(pred_x)-1
        count = 0
        for i in range(1,len(pred_y)):
            if ((test_y[i] >= test_y[i-1]) and (pred_y[i] >= pred_y[i-1])) \
                    or ((test_y[i] < test_y[i-1]) and (pred_y[i] < pred_y[i-1])):
                        count += 1
        print float(count) / denom

	# predictions = optimal_model.predict(test_x)
	pickle.dump(optimal_model, open('models/model.p', 'wb'))
	print optimal_model.coef_
	print optimal_model.score(test_x, test_y)

	# for i in range(len(test_x)):
	# 	print 'price in 10 days is, ', test_y[i]
	# 	print 'price prediction is, ', predictions[i]

	# return model

def main(args):

	x,y = get_features_targets(60,1)
	linear_model(x,y,'lasso','rsquared',[0.70,0.20,0.10], 1000)

	# title = 'Lasso, Values (No Kernel)'
	# deltas = [1,2,3,4,5,6,7,8,9,10]
	# lengths = [30,60,90]
	# test_rsquared = []
	# colors = ['-r','-b','-g']
	# labels = ['30','60','90']
	# for length in lengths:
	# 	tmp = []
	# 	for delta in deltas:
	# 		print delta
	# 		x,y = get_features_targets(length, delta)
	# 		rsquared = linear_model(x,y,'lasso','rsquared',[0.70,0.20,0.10], 10000)
	# 		tmp.append(rsquared)
	# 	test_rsquared.append(tmp)

	# plot([deltas]*3, test_rsquared, colors, labels, title, 'Delta','R Squared')