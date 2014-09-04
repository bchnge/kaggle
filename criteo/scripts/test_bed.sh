### test_bed.sh

############# SAMPLE --> PROCESS --> SELECT --> TRANSFORM --> TRAIN --> PREDICT ##################################

## 0 Draw random sample from train data to be used for testing
####################################################################
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


## 0.5 Preliminary categorical variable selection: Get all categorical features and choose top ones before variable selection
###################################################################
## First create the categorical tables in database
# array=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26)
# for I in "${array[@]}"
# do
# (sqlite3 db/advertising.db "CREATE TABLE ct_c$I (c$I text, Label integer, N integer); INSERT INTO ct_c$I SELECT c$I, Label, count(Id) as N FROM train group by Label,C$I;") 
# done

## Then select top features from the categorical tables
# python src/get_categorical_features.py \
# -d db/advertising.db \
# -f C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -m 10000


## 1 Primary variable selection: Select features using L1 regularized Logistic Regression on training data and also create the subsampled training csv
####################################################################
# python src/extract_features.py \
# -d queries/train_sample.h5 \
# -n I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I13 \
# -c C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 \
# -o features/feat_dict_1.pkl \
# -f data/processed/raw_training_sample.csv \
# -r 0.001


## 2 Transform ALL relevant datasets. this includes training sample, train file, and test file 
####################################################################
# cat data/processed/raw_training_sample.csv | python src/transform.py \
# -f features/feat_dict_1.pkl > data/processed/transformed_training_sample_1.csv & \
# cat data/raw/test.csv | python src/transform.py \
# -f features/feat_dict_1.pkl > data/processed/test_1.csv & \
# cat data/raw/train.csv | python src/transform.py \
# -f features/feat_dict_1.pkl > data/processed/train_1.csv 


## 3 Train your model on the training subsample (in-memory)
####################################################################
python src/train.py \
-i data/processed/transformed_training_sample_1.csv \
-m models/m_2.pkl &


## 4 Classify test set (streaming classifier)
####################################################################
cat data/processed/test_1.csv | python src/classify.py -m models/m_2.pkl -v Id Predicted > submissions/sub_2.csv