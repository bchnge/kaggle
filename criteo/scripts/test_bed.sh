### test_bed.sh


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

# ## Load test data
# python query.py \
# -d advertising.db \
# -t test \
# -f Id I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -s test_queries.h5 \
# -n test_1

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


# ## Extract categorical features and insert into data/categorical_features files
# python src/get_categorical_features.py \
# -d db/advertising.db \
# -f C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -m 10000

# Draw random sample from train data
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



python src/cat_feat_select.py \
-f C1 \
-x 123 \
-a positive_sample_2 \
-b negative_sample_2 

