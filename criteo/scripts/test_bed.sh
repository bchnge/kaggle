#test_bed.sh

# python query.py \
# -d advertising.db \
# -t test \
# -f Id I1 I2 \
# -w "I1 = 1" \
# -l 10 \
# -s test_queries \
# -n q1

# python preview_hdf.py \
# test_queries \
# q1 \
# 10


# python query.py \
# -d advertising.db \
# -t train \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -w "Label = 1" \
# -s train_queries \
# -n positive_sample

# python query.py \
# -d advertising.db \
# -t train \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -w "Label = 0" \
# -s train_queries \
# -n negative_sample

# python preview_hdf.py \
# train_queries \
# positive_sample \
# 10

# There are 11,745,437 positive samples in the training data


# python subsample.py \
# -d advertising.db \
# -t train \
# -n 12000000 \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -w "Label = 0" \
# -s 45840618 \
# -a negative_sample \
# -b train_queries \
# -x 123 

# python preview_hdf.py \
# train_queries \
# negative_sample \
# 10


# 11,745,437 positive samples in training (train_pos)
# 34,095,178 negative samples in training

### Draw random sample from train data
# python subsample.py \
# -d advertising.db \
# -t train_pos \
# -n 1000000 \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -s 11745437 \
# -a positive_sample_1 \
# -b train_queries \
# -x 123 

# python subsample.py \
# -d advertising.db \
# -t train_neg \
# -n 1000000 \
# -f Label I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -s 34095178 \
# -a negative_sample_1 \
# -b train_queries \
# -x 123 

### Load test data
python query.py \
-d advertising.db \
-t test \
-f Id I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
-s test_queries \
-n test_1
