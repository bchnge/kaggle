#!/bin/bash

array=(16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41)
for i in "${array[@]}"
do
(cut -f$i -d, data/train.csv | python src/get_dict.py > data/dicts/dict_$i) &
