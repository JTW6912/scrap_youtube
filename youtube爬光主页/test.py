import pandas as pd

path = 'data.xlsx'
df = pd.read_excel(path)
data = df.values.tolist()

print(data)