import sys
from pandas import DataFrame, HDFStore

store_name = sys.argv[1]
df_name = sys.argv[2]
N = int(sys.argv[3])
print 'Previewing ' + df_name + ' in HDFStore ' + store_name + '...'

store = HDFStore(store_name)
print store[df_name].ix[0:N,:]
store.close()
print 'Done'

