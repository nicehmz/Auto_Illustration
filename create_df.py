import pandas as pd

df1 = pd.read_csv('res1.csv')
df2 = pd.read_csv('res2.csv')
df = pd.concat([df1,df2])
df.to_csv('encode_res.csv',index=False)