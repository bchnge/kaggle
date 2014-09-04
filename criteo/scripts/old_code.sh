# old code



# 11,745,437 positive samples in training (train_pos)
# 34,095,178 negative samples in training

## Draw random sample from train data
# python src/subsample.py \
# -d db/advertising.db \
# -t train_pos \
# -n 500000 \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -s 11745437 \
# -a positive_sample_1 \
# -b queries/train_queries.h5 \
# -x 123 & \
# python src/subsample.py \
# -d db/advertising.db \
# -t train_neg \
# -n 2000000 \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -s 34095178 \
# -a negative_sample_1 \
# -b queries/train_queries.h5 \
# -x 123 


# ## Train model and perform CV 
# python src/cv_analysis.py \
# -f I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -x 123 \
# -a positive_sample_1 \
# -b negative_sample_1 \
# -c test_1 \
# -s submissions/submission_4.csv

# ## Train model and perform CV 
# python src/cv_analysis.py \
# -f I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -x 123 \
# -a positive_sample_1 \
# -b negative_sample_1 \
# -c test_1 \
# -s submissions/submission_5.csv


# # evaluate classifiers
# python src/eval_clf_performance.py \
# -f I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -x 123 \
# -a positive_sample_1 \
# -b negative_sample_1


## Extract categorical features and insert into data/categorical_features files
# python src/get_categorical_features.py \
# -d db/advertising.db \
# -f C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -m 10000

# # Draw random sample from train data
# python src/subsample.py \
# -d db/advertising.db \
# -t train_pos \
# -n 500000 \
# -f Label C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -s 11745437 \
# -a positive_sample_2 \
# -b queries/train_queries.h5 \
# -x 123 & \
# python src/subsample.py \
# -d db/advertising.db \
# -t train_neg \
# -n 2000000 \
# -f Label C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -s 34095178 \
# -a negative_sample_2 \
# -b queries/train_queries.h5 \
# -x 123 

# # Extract selected features
# array=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26)
# for I in "${array[@]}"
# do
# (python src/cat_feat_select.py \
# 	-f C$I \
# 	-x 123 \
# 	-a positive_sample_2 -b negative_sample_2 \
# 	-c 0.001)
# done

# # Draw random sample from train data to be used for testing
# python src/subsample.py \
# -d db/advertising.db \
# -t train_pos \
# -n 250000 \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -s 11745437 \
# -a pos \
# -b queries/train_sample.h5 \
# -x 123 & \
# python src/subsample.py \
# -d db/advertising.db \
# -t train_neg \
# -n 1000000 \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -s 34095178 \
# -a neg \
# -b queries/train_sample.h5 \
# -x 123 

# # Put together all of the numeric and categorical features and save as pickle
# python src/combine_features.py \
# -d queries/train_sample.h5 \
# -n I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -c C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -o queries/data.p

# # Put together all of the numeric and categorical features and save as pickle
# python src/combine_features.py \
# -d queries/test_data.h5 \
# -n I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -c C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -o queries/data_test.p -t


# Convert data pickle as data store
# python src/pickle_to_dataframe.py \
# -i queries/data_test.p \
# -o queries/combined.h5 \
# -n data_test

# # Convert data pickle as data store
# python src/pickle_to_dataframe.py \
# -i queries/data.p \
# -o queries/combined.h5 \
# -n data_1

# # test a classifiers
# python src/eval_clf.py \
# -i queries/combined.h5 \
# -n data_1 \
# -v -s submissions/submission_6.csv



# ## Load test data..
# python src/query_test.py \
# -f data/test.csv \
# -o queries/test_data.h5 \
# -n data





# # Process test data features
# python src/combine_features.py \
# -d queries/test_data.h5 \
# -n I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -c C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -o queries/data_test.p -t


# # Train model
# python src/train.py \
# -i queries/combined.h5 \
# -m models/m_1.pkl \
# -n data_1

# # # Classify a data_test
# python src/classify.py \
# -i queries/combined.h5 \
# -o queries/fitted.h5 \
# -n data_1 \
# -m models/m_1.pkl 


