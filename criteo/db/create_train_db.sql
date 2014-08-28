.separator ","

create table test (Id text primary key, I1 integer, I2 integer, I3 integer, I4 integer, I5 integer, I6 integer, I7 integer, I8 integer, I9 integer, I10 integer, I11 integer, I12 integer, I13 integer, C1 text, C2 text, C3 text, C4 text, C5 text, C6 text, C7 text, C8 text, C9 text, C10 text, C11 text, C12 text, C13 text, C14 text, C15 text, C16 text, C17 text, C18 text, C19 text, C20 text, C21 text, C22 text, C23 text, C24 text, C25 text, C26 text);
.import data/test.csv test

create table train (Id text primary key, Label integer, I1 integer, I2 integer, I3 integer, I4 integer, I5 integer, I6 integer, I7 integer, I8 integer, I9 integer, I10 integer, I11 integer, I12 integer, I13 integer, C1 text, C2 text, C3 text, C4 text, C5 text, C6 text, C7 text, C8 text, C9 text, C10 text, C11 text, C12 text, C13 text, C14 text, C15 text, C16 text, C17 text, C18 text, C19 text, C20 text, C21 text, C22 text, C23 text, C24 text, C25 text, C26 text);
.import data/train.csv train

# Split training data into positive and negative datasets for balanced sampling
create table train_pos (Id text primary key, Label integer, I1 integer, I2 integer, I3 integer, I4 integer, I5 integer, I6 integer, I7 integer, I8 integer, I9 integer, I10 integer, I11 integer, I12 integer, I13 integer, C1 text, C2 text, C3 text, C4 text, C5 text, C6 text, C7 text, C8 text, C9 text, C10 text, C11 text, C12 text, C13 text, C14 text, C15 text, C16 text, C17 text, C18 text, C19 text, C20 text, C21 text, C22 text, C23 text, C24 text, C25 text, C26 text);
insert into train_pos 
	select * from train where Label = 1;

create table train_neg (Id text primary key, Label integer, I1 integer, I2 integer, I3 integer, I4 integer, I5 integer, I6 integer, I7 integer, I8 integer, I9 integer, I10 integer, I11 integer, I12 integer, I13 integer, C1 text, C2 text, C3 text, C4 text, C5 text, C6 text, C7 text, C8 text, C9 text, C10 text, C11 text, C12 text, C13 text, C14 text, C15 text, C16 text, C17 text, C18 text, C19 text, C20 text, C21 text, C22 text, C23 text, C24 text, C25 text, C26 text);
insert into train_neg
	select * from train where Label = 0;

