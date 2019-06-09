import csv
from dateutil import parser
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np


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

# row_a = da.iloc[[0]]
# da.DatetimeIndex
# da.loc[:,'patient']
# row_a['registration_datetime']
# startdate = pd.to_datetime(row_a['registration_datetime'])
# enddate = pd.to_datetime(startdate) + timedelta(hours=1)
# print(len(da.loc[str(startdate):str(enddate)]))

m = np.zeros(len(df))
segment = 0

rowcount = 0
for index, row in da.iterrows():
    if (rowcount > 25000 + 25000 * segment):
        break
    if (rowcount % 2500 == 0):
        print(rowcount)
    #     break
    # mask=(da['registration_datetime'] > '2018-06-28 01:38') & (da['registration_datetime'] <= '2018-06-30')
    # print(da.loc[mask])

    eventdate = pd.to_datetime(index)
    startdate = eventdate

    # startdate = pd.to_datetime('2018-06-28 01:38:08')
    enddate = pd.to_datetime(startdate) + timedelta(hours=1)
    # df = df.set_index(['registration_datetime'])

    # print(rowcount, startdate, enddate, index, row['patient'], len(
    #     da.loc[str(startdate):str(enddate)]))
    # print(da.loc[str(startdate):str(enddate)])
    # print(df.loc[str(startdate):str(enddate)])

    m[rowcount] = len(
        da.loc[str(startdate):str(enddate)])

    rowcount += 1

# This does not work
# da['old'] = len(
# da.loc[da['registration_datetime']:str(pd.to_datetime(da['registration_datetime'])
# + timedelta(hours=1))])

# da = da.assign(e=p.Series(np.random.randn(sLength)).values)


# for i in range(1, len(df)):
# df.loc[i, 'C'] = df.loc[i-1, 'C'] * df.loc[i, 'A'] + df.loc[i, 'B']


# with open('Data/ERlast2years.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     size = 5
#     row = [None]*size
#     initrow = 0
# #	print(row)
#     for rowIn in reader:
#         if initrow == 0:
#             row[0] = rowIn

#             initrow = 1
#             print("first run")
#             continue
#         else:
#             row[1] = rowIn
#             print(pd.to_datetime(row[1]['registration_datetime']) -
#                   pd.to_datetime(row[0]['registration_datetime']))

#             row[0] = row[1]
