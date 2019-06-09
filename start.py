import csv
from dateutil import parser
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd
from datetime import datetime, timedelta

#  df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')


parse_dates = ['registration_datetime', 'traige_datetime', 'discharge_datetime', 'closing_of_ed_record_datetime', 'arrival_at_department_datetime',
               'actual_transfer_datetime', 'nursing_care_report_start_of_reporting_datetime', 'receivement_approvement_of_first_sampling', 'last_results_document_creation_hour']

df = pd.read_csv('../ERlast2years.csv',
                 parse_dates=parse_dates, low_memory=False, dtype={})
# , dtype={"hospitalization_department": str, "planned_transfer_date": str, "minutes_from_admittance_to_discharge": str, "referrer": str, "triage_urgency": int32})

df = df.set_index(['registration_datetime'])


da = df.copy()


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


# mask=(da['registration_datetime'] > '2018-06-28 01:38') & (da['registration_datetime'] <= '2018-06-30')
# print(da.loc[mask])
startdate = pd.to_datetime('2018-06-28 01:38:08')
enddate = pd.to_datetime(startdate) + timedelta(hours=1)
print(df.loc[str(startdate):str(enddate)])


for index, row in df.iterrows():
    print(row['c1'], row['c2'])

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
