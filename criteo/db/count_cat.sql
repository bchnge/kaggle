-- CREATE TABLE ct_c1 (C1 text, N integer);
-- INSERT INTO ct_c1
-- 	SELECT C1,count(ID) as N
-- 	FROM train
-- 	GROUP BY C1
-- 	;


CREATE TABLE ct_c2 (C2 text, N integer);
INSERT INTO ct_c2
	SELECT C2,count(ID) as N
	FROM train
	GROUP BY C2
	;
