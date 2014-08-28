# test_bed.sh


# 11,745,437 positive samples in training (train_pos)
# 34,095,178 negative samples in training

# ## Draw random sample from train data
# python subsample.py \
# -d advertising.db \
# -t train_pos \
# -n 1000000 \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -s 11745437 \
# -a positive_sample_1 \
# -b train_queries.h5 \
# -x 123 

# python subsample.py \
# -d advertising.db \
# -t train_neg \
# -n 1000000 \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -s 34095178 \
# -a negative_sample_1 \
# -b train_queries.h5 \
# -x 123 

# ## Load test data
# python query.py \
# -d advertising.db \
# -t test \
# -f Id I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -s test_queries.h5 \
# -n test_1
