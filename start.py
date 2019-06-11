import csv
from dateutil import parser
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

import numpy as np
import time


import pandas as pd
from datetime import datetime, timedelta


parse_dates = ['registration_datetime', 'traige_datetime', 'discharge_datetime', 'closing_of_ed_record_datetime', 'arrival_at_department_datetime',
               'actual_transfer_datetime', 'nursing_care_report_start_of_reporting_datetime', 'receivement_approvement_of_first_sampling', 'last_results_document_creation_hour']

df = pd.read_csv('Data/ERlast2years.csv',
                 parse_dates=parse_dates, low_memory=False)

# , dtype={"hospitalization_department": str, "planned_transfer_date": str, "minutes_from_admittance_to_discharge": str, "referrer": str, "triage_urgency": int32})


df = df.sort_values('registration_datetime')


da = df[['registration_datetime', 'patient']].copy()


############################# Begin Group by Day/Hour  #############################
# If going to do resampling
# This method gets the number of events in a small amount of time such as a day or an hour
# Then we look at all the days that have spikes higher than two standard deviations above the mean.
# That is they are Improbable and are noise
#
# def countLines(array):
#     return len(array)
# da = df[['registration_datetime', 'patient']].resample('D', on='registration_datetime').apply(countLines)
# df[['registration_datetime','patient']].resample('60min', on='registration_datetime').apply(countLines)
# plot([1,2,3], [1,2,3], 'go-', label='line 1', linewidth=2)
# da = da.set_index(['registration_datetime'])

# Plot the resamle
# data = [go.Scatter(x=da['registration_datetime'], y=da['patient'])]
# py.iplot(data, filename='time-series-simple')

# spikes = da.loc[(da['patient'] >= da.mean()['patient'] + 2 * da.std()
############################# End Group by Day/Hour  #############################


# Iterate through each row and search for the items that are
# in proximity by using a date ran

da = da.set_index(['registration_datetime'])


visitorCount = np.zeros(len(df))

start = time.time()
rowcount = 0
for index, row in da.iterrows():
    if (rowcount % 2500 == 0):
        end = time.time()
        print(end - start, rowcount)
        start = time.time()

    #     break
    # mask=(da['registration_datetime'] > '2018-06-28 01:38') & (da['registration_datetime'] <= '2018-06-30')
    # print(da.loc[mask])

    eventdate = pd.to_datetime(index)
    startdate = eventdate - timedelta(hours=1)

    # startdate = pd.to_datetime('2018-06-28 01:38:08')
    enddate = eventdate + timedelta(hours=1)
    # df = df.set_index(['registration_datetime'])

    # print(rowcount, startdate, enddate, index, row['patient'], len(
    #     da.loc[str(startdate):str(enddate)]))
    # print(da.loc[str(startdate):str(enddate)])

    visitorCount[rowcount] = len(
        da.loc[str(startdate):str(enddate)])

    rowcount += 1

if 1 == 0:
    dvisitors = pd.read_csv('Results/DVWithVititsInHour.csv',
                            low_memory=False)

else:
    df['visits_within_hour'] = visitorCount
    # df.to_csv('Results/DVWithVititsInHour.csv')

spikes = df.loc[(df['visits_within_hour'] >= df.mean()[
                 'visits_within_hour'] + 2 * df.std()['visits_within_hour'])]

df[['visits_within_hour', 'patient']].groupby('visits_within_hour').count()


a = df['visits_within_hour'].values.tolist()

# py.iplot(ff.create_distplot([a[c] for c in a.columns], a.columns, bin_size=1),
#          filename='distplot with pandas')

# begin example
x = np.random.randn(1000)
hist_data = [x]
group_labels = ['distplot']

fig = ff.create_distplot(hist_data, group_labels)
py.iplot(fig, filename='Basic Distplot')
# End Example

# data=[go.Scatter(x=df['registration_datetime'], y=df['visits_within_hour'])]
# data = [go.Scatter(x=dff['registration_datetime'], y=dff['visits_within_hour'])]

py.iplot(data, filename='time-series-simple')

if 1 == 0:
    df.corr().to_csv('Results/Correlation With VisitsWithinHour.csv')
