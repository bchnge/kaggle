# To do
--------

Test benefit of votingensemble with different combinations
gridsearch with different model weights and different combinations


supplementary data:
    Add mean, min, max 
    Add lableler for categorial
    
Try ensembling different models with different features (stacking)
M3 = f(M1, M2)


Choose a relatively high learning rate. Generally a learning rate of 0.1 works but somewhere between 0.05 to 0.3 should work for different problems. Determine the optimum number of trees for this learning rate. XGBoost has a very useful function called as “cv” which performs cross-validation at each boosting iteration and thus returns the optimum number of trees required.
Tune tree-specific parameters ( max_depth, min_child_weight, gamma, subsample, colsample_bytree) for decided learning rate and number of trees. Note that we can choose different parameters to define a tree and I’ll take up an example here.
Tune regularization parameters (lambda, alpha) for xgboost which can help reduce model complexity and enhance performance.
Lower the learning rate and decide the optimal parameters .



# Meaningful features
-------------------------
AMT_CREDIT / AMT_ANNUITY
DAYS_ENTRY_PAYMENT/DAYS_DECISION
AMT_PAYMENT_mean / AMT_INSTALMENT
DAYS_DECISION_max / DAYS_ENTRY_PAYMENT
DAYS_ENTRY_PAYMENT / DAYS_INSTALMENT_mean
AMT_PAYMENT_mean / AMT_ANNUITY_1
DAYS_ENTRY_PAYMENT_mean / DAYS_LAST_PHONE_CHANGE


AMT_ANNUITY / AMT_GOODS_PRICE
NUM_INSTALMENT_NUMBER_mean / CNT_PAYMENT_max
CNT_INSTALMENT_FUTURE_mean / CNT_INSTALMENT_FUTURE_max

NUM_INSTALMENT_NUMBER_mean / CNT_PAYMENT_max
CNT_PAYMENT_mean / CNT_INSTALMENT_FUTURE_mean
CNT_INSTALMENT_FUTURE_mean / CNT_INSTALMENT_FUTURE_max

AMT_INSTALMENT_MAX / AMT_ANNUITY_mean
