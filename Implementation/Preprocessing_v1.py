import pandas as pd
import datetime as dt

# Read the csv file regarding the weather at Wind turbine's territory
weather = pd.read_csv("weather.csv")

# Drop the unnecessary columns
wt = weather.drop(columns=['wind_speed1', 'temperature1'])

# Convert the date to a proper form with datetime and extract the time
wt['Date'] = pd.to_datetime(wt['Date'])
wt['Date'] = wt['Date'].apply(lambda x: x.replace(year = x.year + 8))
wt[['Date1', 'Time']] = wt.Date.astype(str).str.split(' ', 1, expand=True)
del wt['Date']

# Place the Date and Time columns as the first columns of our dataframe
cols = list(wt.columns)
a, b, c, d = cols.index('pressure'), cols.index('Date1'), cols.index('roughness_length'), cols.index('Time')
cols[a], cols[b], cols[c], cols[d] = cols[b], cols[a], cols[d], cols[c]
wt = wt[cols]

# Extract the time and add the time difference we discarded
for i in range(0, len(wt.Time)):

    wt.iloc[i, 1] = str(wt.iloc[i, 1])[0:8]
    wt.iloc[i, 1] = pd.to_datetime(wt.iloc[i, 1]) + dt.timedelta(hours=1)
    wt.iloc[i, 1] = wt.iloc[i, 1].time()

# Rename the columns
wt.rename(columns={'Date1':'Date',
                    'temperature2':'Temperature (K)',
                    'wind_speed2':'Wind_speed (m/s)',
                    'pressure':'Pressure (Pa)',
                     'roughness_length':'Roughness_length (m)'}, inplace=True)

# print(wt.Time.head())

# Store the reformed dataframe in a csv file
wt.to_csv('weather_final.csv')
