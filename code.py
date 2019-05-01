#!/usr/bin/env python
# coding: utf-8

# # Flights Data Exploration
# ## Preliminary Wrangling
# >This dataset reports flights in the United States, including carriers, arrival and departure delays, and reasons for delays, from 1987 to 2008.
# #### Variable descriptions

# | --- | **Name** | **Description** |
# | --- | --- | --- |
# | 1 | Year | 1987-2008 |
# | 2 | Month | 1-12 |
# | 3	| DayofMonth | 1-31 |
# | 4 | DayOfWeek	| 1 (Monday) - 7 (Sunday) |
# | 5	| DepTime | actual departure time (local, hhmm) |
# | 6	| CRSDepTime | scheduled departure time (local, hhmm) |
# | 7	| ArrTime | actual arrival time (local, hhmm) |
# | 8	| CRSArrTime | scheduled arrival time (local, hhmm) |
# | 9	| UniqueCarrier | unique carrier code |
# | 10 | FlightNum | flight number |
# | 11 | TailNum | plane tail number |
# | 12 | ActualElapsedTime | in minutes |
# | 13 | CRSElapsedTime | in minutes |
# | 14 | AirTime | in minutes |
# | 15 | ArrDelay | arrival delay, in minutes |
# | 16 | DepDelay | departure delay, in minutes |
# | 17 | Origin | origin IATA airport code |
# | 18 | Dest | destination IATA airport code |
# | 19 | Distance | in miles |
# | 20 | TaxiIn | taxi in time, in minutes |
# | 21 | TaxiOut | taxi out time in minutes |
# | 22 | Cancelled | was the flight cancelled? |
# | 23 | CancellationCode | reason for cancellation (A = carrier, B = weather, C = NAS, D = security) |
# | 24 | Diverted | 1 = yes, 0 = no |
# | 25 | CarrierDelay | in minutes |
# | 26 | WeatherDelay | in minutes |
# | 27 | NASDelay | in minutes |
# | 28 | SecurityDelay | in minutes |
# | 29 | LateAircraftDelay | in minutes |

# In[1]:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import calendar

%matplotlib inline

# In[2]:
df_2008 = pd.read_csv('2008.csv')

# In[3]:
print(df_2008.shape)
print(df_2008.dtypes)
print(df_2008.head(10))

# In[4]:
# Due to large file size, take a sample to more efficiently analyze trends in data
df_2008.sample(100000).to_csv('2008_sampled_100000.csv')

# In[5]:
df_2008s = pd.read_csv('2008_Sampled_100000.csv')

# In[6]
print(df_2008s.shape)
print(df_2008s.dtypes)
print(df_2008s.head(10))
print(df_2008s.describe())

# ### What is the structure of your dataset?
# >There are 7,009,728 flights in this dataset with 25 features (Year, Month, Day of Month, Day Of Week, Actual Departure Time, Scheduled Departure Time, Actual Arrival Time, Scheduled Arrival Time, Unique Carrier Code, Flight Number, Plane Tail Number, Actual Elapsed Time, Scheduled Elapsed Time, Air Time, Arrival Delay, Departure Delay, Origin, Destination, Distance, Taxi in time, Taxi Out Time, Cancelled, Reason For Cancellation (A = carrier, B = weather, C = NAS, D = security), Diverted, Carrier Delay, Weather Delay, NAS Delay, Security Delay, Late Aircraft Delay.

# ### What is/are the main feature(s) of interest in your dataset?
# >I am most interested in figuring out what features are best for predicting the likelihood a flight is delayed or cancelled. I am also interested in the proportion of delays and cancellations for day of week and month of year.

# ### What features in the dataset do you think will help support your investigation into your feature(s) of interest?
# I expect that weather delays and number of flights will have the strongest effect on delay or cancellation. This means that the **CancellationCode** column and each of the delay columns will be of interest. To calculate the number of flights, I plan to use the `.value_counts()` on the **Month** and **DayOfWeek** columns.

# ## Univariate Exploration
# In[7]:
# Making sure that we're converting numbers to days/months correctly
days = list(calendar.day_name)
days_abbr = list(calendar.day_abbr)
print(days, days_abbr)
month = list(calendar.month_name)
month_abbr = list(calendar.month_abbr)
print(month, month_abbr)
print(calendar.month_abbr[1])
exit()

# In[8]:
# Calculating how many flights there are per month.
df_2008s_month_value_counts = df_2008s.Month.value_counts().reset_index()
df_2008s_month_value_counts.columns = ["Month", "Total_Flights"]
df_2008s_month_value_counts = df_2008s_month_value_counts.sort_values(by=['Month'])
df_2008s_month_value_counts['Month'] = df_2008s_month_value_counts['Month'].apply(lambda x: calendar.month_abbr[x])
print(df_2008s_month_value_counts)
df_flights_by_month = df_2008s_month_value_counts.reset_index()
df_flights_by_month = df_flights_by_month.drop(columns=['index'])
df_flights_by_month


# In[9]:
# Plot month value counts as bar plot
df_2008s_month_value_counts.plot(kind='bar', x='Month', y='Total_Flights', color = 'teal', legend=False)
plt.title("Total Flights by Month")
plt.ylabel("Total Flights")
plt.xlabel("")
plt.show();


# In[10]:
######### Day of the Week
# Calculating how many flights there are per day of week.
df_2008s_day_value_counts = df_2008s.DayOfWeek.value_counts().reset_index()
df_2008s_day_value_counts.columns = ["DayOfWeek", "Total_Flights"]
df_2008s_day_value_counts = df_2008s_day_value_counts.sort_values(by=['DayOfWeek'])
df_2008s_day_value_counts['DayOfWeek'] = df_2008s_day_value_counts['DayOfWeek'].apply(lambda x: calendar.day_abbr[x-1])
print(df_2008s_day_value_counts)


# In[11]:
# Plot day value counts as bar plot
df_2008s_day_value_counts.plot(kind='bar', x='DayOfWeek', y='Total_Flights', color = 'teal', legend=False)
plt.title("Total Flights by Day of Week")
plt.ylabel("Total Flights")
plt.xlabel("")
plt.show();


# In[12]:
######### Day of the Year
# Calculating how many flights there are per day of year.
df_dvc2 = df_2008s
df_dvc2['Date']=df_dvc2['Year'].astype(str)+'/'+df_dvc2['Month'].astype(str)+'/'+df_dvc2['DayofMonth'].astype(str)
df_dvc2 = df_dvc2.Date.value_counts().reset_index()
df_dvc2.columns = ["Day", "Total_Flights"]
df_dvc2['Date'] = pd.to_datetime(df_dvc2['Day'], format='%Y/%m/%d')
df_dvc2 = df_dvc2.sort_values(by=['Day'])
print(df_dvc2)


# In[13]:
# Plot day value counts as bar plot
df_dvc2.plot(kind='line', x='Day', y='Total_Flights', color = 'teal', legend=False, figsize = (16,10))
plt.title("Total Flights by Day of Year")
plt.ylabel("Total Flights")
plt.xlabel("")
plt.show();


# In[14]:
# Total Cancellations
df_2008s.Cancelled.unique()


# In[15]:
df_cancelled = df_2008s['Cancelled'].value_counts()
df_cancelled = df_cancelled.reset_index()
df_cancelled


# In[16]:
cancelled_percent = df_cancelled.Cancelled[1] / (df_cancelled.Cancelled[0] + df_cancelled.Cancelled[1]) * 100
cancelled_percent = str(round(cancelled_percent, 2)) + "%"
cancelled_percent

# In[17]:
not_cancelled_percent = df_cancelled.Cancelled[0] / (df_cancelled.Cancelled[0] + df_cancelled.Cancelled[1]) * 100
not_cancelled_percent = str(round(not_cancelled_percent, 2)) + "%"
not_cancelled_percent

# In[18]:
df_cancelled.Cancelled.plot(kind= 'pie', labels = ['Not Cancelled (' + not_cancelled_percent + ')', 'Cancelled (' + cancelled_percent + ')'], figsize=(8,8))
plt.title("Percentage of Flights that are Cancelled")
plt.ylabel("");

# >1.96% of all flights are cancelled. That is almost two flights per one hundred.

# In[19]:
# Mean Cancellations
df_2008s.Cancelled.mean()


# In[20]:
# Cancellations by Cancellation Code
df_2008s['CancellationCode'].value_counts()


# In[21]:
df_2008s['CancellationCode'].replace({'A': 'carrier', 'B': 'weather', 'C': 'NAS', 'D': 'security'}, inplace = True)


# In[22]:
# A = carrier, B = weather, C = NAS, D = security
df_2008s['CancellationCode'].value_counts().plot(kind= 'bar', color = 'teal', figsize=(8,8))
plt.title("Causes of Flight Cancellations")
plt.ylabel("Count")
plt.xlabel("Type of Cancellation")
plt.show();


# In[23]:
# Carrier Delays
df_cd_1 = df_2008s.query('CarrierDelay != "NaN"')
df_cd_1 = df_cd_1.query('CarrierDelay != "0.0"')
df_cd_1


# In[24]:
df_cd_1.describe().CarrierDelay


# In[25]:
bin_edges = [1, 9, 19, 41, 2436]
bin_names = ['1-8', '9-18', '19-39', '40-1951']
df_cd_1['CDGroup'] = pd.cut(df_cd_1['CarrierDelay'], bin_edges, labels=bin_names)
df_cd_1


# In[26]:
df_cd_1['CDGroup'].value_counts()


# In[27]:
df_cd_1['CDGroup'].value_counts(sort = False).plot(kind= 'bar', color = 'teal', figsize=(8,8))
plt.title("Length of Carrier Delay")
plt.ylabel("Count")
plt.xlabel("Length of Delay (min)")
plt.show();


# In[28]:
# Weather Delays
df_wd_1 = df_2008s.query('WeatherDelay != "NaN"')
df_wd_1 = df_wd_1.query('WeatherDelay != "0.0"')
df_wd_1


# In[29]:
df_wd_1.describe().WeatherDelay


# In[30]:
bin_edges = [1, 11, 25, 57, 1352]
bin_names = ['1-10', '11-24', '25-56', '57-1352']
df_wd_1['WDGroup'] = pd.cut(df_wd_1['WeatherDelay'], bin_edges, labels=bin_names)
df_wd_1


# In[31]:
df_wd_1['WDGroup'].value_counts()


# In[32]:
df_wd_1['WDGroup'].value_counts(sort = False).plot(kind= 'bar', color = 'teal', figsize=(8,8))
plt.title("Length of Weather Delay")
plt.ylabel("Count")
plt.xlabel("Length of Delay (min)")
plt.show();


# In[33]:
# NAS Delays
df_nd_1 = df_2008s.query('NASDelay != "NaN"')
df_nd_1 = df_nd_1.query('NASDelay != "0.0"')
df_nd_1


# In[34]:
df_nd_1.describe().NASDelay


# In[35]:
bin_edges = [1, 8, 18, 31, 1357]
bin_names = ['1-7', '8-17', '18-30', '31-1357']
df_nd_1['NDGroup'] = pd.cut(df_nd_1['NASDelay'], bin_edges, labels=bin_names)
df_nd_1


# In[36]:
df_nd_1['NDGroup'].value_counts()


# In[37]:
df_nd_1['NDGroup'].value_counts(sort = False).plot(kind= 'bar', color = 'teal', figsize=(8,8))
plt.title("Length of NAS Delay")
plt.ylabel("Count")
plt.xlabel("Length of Delay (min)")
plt.show();


# In[38]:
# Security Delays
df_sd_1 = df_2008s.query('SecurityDelay != "NaN"')
df_sd_1 = df_sd_1.query('SecurityDelay != "0.0"')
df_sd_1


# In[39]:
df_sd_1.describe().SecurityDelay


# In[40]:
bin_edges = [1, 7, 13, 22, 392]
bin_names = ['1-6', '7-12', '13-21', '22-392']
df_sd_1['SDGroup'] = pd.cut(df_sd_1['SecurityDelay'], bin_edges, labels=bin_names)
df_sd_1


# In[41]:
df_sd_1['SDGroup'].value_counts()