numeric_dict = {}
categorical_dict = {}
# Initialize dictionary

numeric_dict = {'count': {}, 'sum':{}}
numeric_fields = ['I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13']
for field in numeric_fields:
	numeric_dict['count'][field] = 1
	numeric_dict['sum'][field] = 0

import numpy as np
row = ['24', '3','', '123' ,'5','3', '25', '123', '6', '4', '12','3','7']
ones = list(1-(np.array(row) == ''))
vals = [int(x) if x != '' else 0 for x in row]
print ones
print len(row)

numeric_dict['count'] = zip(numeric_fields, [sum(x) for x in zip(numeric_dict['count'].values(), list(ones))])
numeric_dict['sum'] = zip(numeric_fields, [sum(x) for x in zip(numeric_dict['sum'].values(), list(vals))])

print numeric_dict




# categorical_fields = ['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21', 'C22', 'C23', 'C24','C25','C26']
# for field in categorical_fields:
# 	categorical_dict[field] = {''}

# row =['c1','','c2','wef12','afbesf','awef21','asdf','c3','c5','c5','1','135','12312f','1241f','sdfs12','f23','241d','1d','dsf2','asd23','df32r32r','12rf','12e1f','12r12r12r','2f23','1fr']



# new_row2 =['casdf1','sda','casdfwe2','w12eef12','afasdvbesf','a12ewef21','a124123sdf','c31231','c512','c1235','1123v','112r35','12312f','1241f','sdfsds12','f23','241d','1d','dsf2','asd23','df32r32r','12rf','12e1f','12r12r12r','2f23','1fr']

# # for item in zip(categorical_fields, row):
# # 	categorical_dict[item[0]].update([item[1]])

# # for item in zip(categorical_fields, new_row2):
# # 	categorical_dict[item[0]].update([item[1]])

# # categorical_dict[item[0]].update([item[1]]) for item in zip(categorical_fields, row)

# # for item in zip(categorical_fields, new_row2):
# # 	categorical_dict[item[0]].update([item[1]])


# print categorical_dict.items()
# fields = ['Id']
# print row
# print row[2:3]
# print row[5:]

