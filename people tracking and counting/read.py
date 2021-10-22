import pandas as pd
#df = pd.read_csv('Allrecap\Allrecap.csv')
header_names = ['value', 'date', 'time']
df = pd.read_csv('Allrecap\Allrecap.csv', header = None, skiprows=1, names=header_names)
#df.head()
value_sum = df['value'].sum()
value_mean = df['value'].mean()

#print(value_sum)
#print(value_mean)
df['time']=pd.to_datetime(df['time'])
minute = df['time'].dt.minute
hour = df['time'].dt.hour
minute_tail = minute.tail(1)
minute_head = minute.head(1)
minute_estimation = minute_tail - minute_head

print(minute_estimation)
