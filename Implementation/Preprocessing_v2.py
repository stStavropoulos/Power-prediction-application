import pandas as pd

# Read the csv file regarding the wind turbine's functionality and extract the date and time
wp = pd.read_csv("WindPower.csv")
wp['Date/Time'] = pd.to_datetime(wp['Date/Time'])
wp[['Date', 'Time']] = wp['Date/Time'].astype(str).str.split(' ', 1, expand=True)
del wp['Date/Time']

# Keep only the samples for each hour and discard the rest
str_list = []
int_list = []
for i in wp.Time:
    str_list.append(str(i))

for i in range(0, len(str_list)):
    if str_list[i][3] == '0':
        int_list.append(i)

filter_wp = wp[wp.index.isin(int_list)]
filter_wp.reset_index(drop=True, inplace=True)

# Place the Date and Time columns as the first columns of our dataframe
cols = list(filter_wp.columns)
a, b, c, d = cols.index('LV ActivePower (kW)'), cols.index('Date'), cols.index('Wind Speed (m/s)'), cols.index('Time')
cols[a], cols[b], cols[c], cols[d] = cols[b], cols[a], cols[d], cols[c]
filter_wp = filter_wp[cols]

# Store the reformed dataframe in a csv file
filter_wp.to_csv('Power_final.csv')

# Read the two csv files
wt = pd.read_csv("weather_final.csv")
wp = pd.read_csv("Power_final.csv")

# Drop the duplicates
wt.drop(['Date', 'Time', 'Wind_speed (m/s)'], axis=1, inplace=True)
wp.drop([0])
wp.reset_index(inplace=True)

# Merge and store to the final file
wind = pd.merge(wp, wt)
wind.drop('Unnamed: 0', axis=1, inplace=True)
wind.to_csv("WindData.csv")
# print(wind.shape)
