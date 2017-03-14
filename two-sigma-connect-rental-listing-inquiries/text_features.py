import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import calendar
import datetime
from pprint import pprint
from scipy.stats import binom_test

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



def main():
	df = pd.read_json('train.json')
	y = df.interest_level
	x = df.description
	print df.columns

	vect = CountVectorizer(ngram_range = (2,2), max_features = 100, stop_words = 'english')

	X_train_counts = vect.fit_transform(x)

	print X_train_counts


	pprint(vect.vocabulary_)
	print X_train_counts.shape


if __name__ == '__main__':
	main()


