import pandas as pd
import numpy as np
import calendar
import datetime
from pprint import pprint
from scipy.stats import binom_test
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, log_loss


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def proportion(x, precision = 1):
	result = np.mean(x) * 100
	result = result.round(precision)
	return result



def get_summary(grouped_df):

# 'pval': lambda x: binom_test(np.sum(x), np.count_nonzero(x), 0.33)
	return grouped_df['interest_high','interest_medium','interest_low'].agg({'interest_share' : lambda x: proportion(x,precision = 1), 'count': np.count_nonzero, })

def main():
	df = pd.read_json('data/train.json')

	clusters = np.genfromtxt('clusters.results', delimiter = ',')

	print '\n---Summary of numeric data---'
	print df.describe()

	variables = df.columns


	print "\n---Unique values---"
	variables = [v for v in variables if v not in ['listing_id', 'photos', 'display_address', 'features', 'street_address', 'description']]

	for v in variables:
		print v + ': ' + str(df[v].nunique())

	# Generate some basic features from existing variables
	df['created'] = pd.to_datetime(df['created'])

	df['listing_age'] = df['created'].max() - df['created']
	df['listing_age'] = df['listing_age'].apply(lambda x: x.days)

	df['num_photos'] = df.photos.apply(lambda x: len(x))

	df['created_month'] = df['created'].dt.month.apply(lambda x: calendar.month_abbr[x])
	df['created_day'] = df['created'].dt.day
	df['created_dow'] = df['created'].dt.weekday

	df['interest_high'] = df['interest_level'] == 'high'
	df['interest_medium'] = df['interest_level'] == 'medium'
	df['interest_low'] = df['interest_level'] == 'low'

	deciles = [float(i)/100 for i in range(0,100,5)]
	qtiles = [float(i)/100 for i in range(0,100,5)]

	df['price_deciles'] = pd.qcut(df['price'], q = deciles, labels = False)

	df['description_length'] = df.description.apply(lambda x: len(x))
	df['description_length_qtiles'] = pd.qcut(df['description_length'], q = qtiles, labels = False)

	df['listing_age_qtiles'] = pd.qcut(df['listing_age'], q = qtiles, labels = False)

	df['db_cluster'] = pd.Series(clusters)

	df['features_str'] = df['features'].apply(lambda x: ','.join(x))
	df['features_str'] = df['features_str'].apply(lambda x: x.lower().strip())

	def comma_tokenizer(s):
		return s.split(',')


	# Process listing features		
	from sklearn.feature_extraction.text import CountVectorizer

	vect = CountVectorizer(tokenizer = comma_tokenizer, ngram_range = (2,4), max_features = 500, binary = True)

	features = vect.fit_transform(df['features_str'])


	# Bivariate relationships
	x_vars = ['price_deciles', 'created_month', 'bedrooms', 'bathrooms', 'num_photos', 'listing_age_qtiles', 'created_day', 'created_dow', 'description_length_qtiles', 'db_cluster']

	from bokeh.charts import Bar, Scatter
	from bokeh.plotting import figure, output_file, show
	from bokeh.resources import CDN
	from bokeh.layouts import row
	from bokeh.embed import file_html

	print '\n---Bivariate relationships---'
	for x in x_vars:
		print '\n------' + x + '------'
		print get_summary(df.groupby(x))



	def plotGroupBy(x):
		tmp = get_summary(df.groupby(x))['interest_share']
		tmp[x] = tmp.index
		p1 = Bar(tmp, x, color = 'navy', values = 'interest_high', title = 'High interest by ' + x, legend = False)
		p2 = Bar(tmp, x, color = 'firebrick', values = 'interest_medium', title = 'Medium interest by ' + x, legend = False)
		p3 = Bar(tmp, x, color = 'olive', values = 'interest_low', title = 'Low interest by ' + x, legend = False)
		return row(p1,p2,p3)

	myPlots = [plotGroupBy(x) for x in x_vars]

	html = file_html(myPlots, CDN, x)

	with open('content/edaPlots.html', 'w') as f:
		f.write(html)


	# model_lr = LogisticRegression()
	# model_lr.fit(X = features, y = df.interest_level.values)
	# print model_lr.coef_

	# print model_lr.score(features, df.interest_level.values)

	# fitted = model_lr.predict(features)
	# fitted_probs = model_lr.predict_proba(features)
	# print confusion_matrix(df.interest_level.values, fitted)

	# print log_loss(df.interest_level.values, fitted_probs)

	print features.shape
	print vect.vocabulary_.keys()
#	np.savetxt('features.csv', features.toarray(), delimiter = ',')
	dataFrame = pd.DataFrame(data = features.toarray(), columns = vect.vocabulary_.keys())
	dataFrame['interest_level'] = df['interest_level'].values

	dataFrame.to_csv('features.csv', index = False)



if __name__ == '__main__':
	main()


