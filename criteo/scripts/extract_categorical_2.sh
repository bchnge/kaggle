#!/bin/bash

array=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26)

for I in "${array[@]}"
do
(sqlite3 advertising.db "CREATE TABLE pct_c$I (c$I text, N integer, PctPos real); INSERT INTO pct_c$I SELECT C$I, sum(N) as N, sum(Label*N)*1.0/sum(N) as PctPos FROM ct_c$I GROUP BY C$I ORDER BY PctPos DESC;") 
done