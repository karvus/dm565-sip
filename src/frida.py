import pandas

df = pandas.read_csv('Frida20190802dav3.csv')
new_cols = df.columns.values
new_cols[0] = "nummer"
new_cols[1] = "gruppe"
new_cols[2] = "navn"
df.columns = new_cols
print(df.loc[1])
print(df[df['navn'].str.contains(u'Quinoa')])



