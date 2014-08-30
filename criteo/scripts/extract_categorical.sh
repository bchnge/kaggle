#!/bin/bash

# array=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26)
array=(13 14 15 16 17 18)
for I in "${array[@]}"
do
(sqlite3 advertising.db "DROP TABLE ct_c$I; CREATE TABLE ct_c$I (c$I text, Label integer, N integer); INSERT INTO ct_c$I SELECT c$I, Label, count(Id) as N FROM train group by Label,C$I;") 
done