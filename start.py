import csv
# from dateutil import parser
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

import numpy as np
import time
import hebcal


import pandas as pd
from datetime import datetime, timedelta


parse_dates = ['registration_datetime', 'traige_datetime', 'discharge_datetime', 'closing_of_ed_record_datetime', 'arrival_at_department_datetime',
               'actual_transfer_datetime', 'nursing_care_report_start_of_reporting_datetime', 'receivement_approvement_of_first_sampling', 'last_results_document_creation_hour']

df = pd.read_csv('Data/ERlast2years.csv',
                 parse_dates=parse_dates, low_memory=False)

# , dtype={"hospitalization_department": str, "planned_transfer_date": str, "minutes_from_admittance_to_discharge": str, "referrer": str, "triage_urgency": int32})


df = df.sort_values('registration_datetime')


# df[df.index==1]['registration_datetime'].to_string()
# hebcal.TimeInfo(df[df.index==1]['registration_datetime'].to_string(), timezone='Asia/Jerusalem', longitude=35.2137, latitude=31.7683)
# hebcal.calendar.is_holiday()
# def isHoliday(dateString):
#     return hebcal.calendar.is_holiday(hebcal.TimeInfo(dateString.strftime("%H:%M:%S.%f - %b %d %Y"), timezone='Asia/Jerusalem', longitude=35.2137, latitude=31.7683))
# df['holday'] =


df['dthour'] = df['registration_datetime'].dt.hour
df['dtmonth'] = df['registration_datetime'].dt.month
df['dtweekday'] = df['registration_datetime'].dt.weekday
# This has monday = 0
seasons = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 1]
month_to_season = dict(zip(range(1, 13), seasons))
df['dtseason'] = df['registration_datetime'].dt.month.map(month_to_season)

# df['day_of_week'] = df['registration_datetime'].dt.day_name()
df['hourofweek'] = df.apply(lambda x: "%02d%02d" %
                            (x['dtweekday'], x['dthour']), axis=1)

############################# Begin Group by Day/Hour  #############################
# If going to do resampling
# This method gets the number of events in a small amount of time such as a day or an hour
# Then we look at all the days that have spikes higher than two standard deviations above the mean.
# That is they are Improbable and are noise
#


# def countLines(array):
#     return len(array)


# dg = df[['registration_datetime', 'patient']].resample(
#     '30min', on='registration_datetime').apply(countLines)


dg = df[['registration_datetime', 'minutes_from_admittance_to_discharge']].resample(
    '60min', on='registration_datetime').count()

dg['registration_datetime'] = dg.index

dg['dthour'] = dg['registration_datetime'].dt.hour
dg['dtmonth'] = dg['registration_datetime'].dt.month
dg['dtweekday'] = dg['registration_datetime'].dt.weekday
# This has monday = 0
seasons = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 1]
month_to_season = dict(zip(range(1, 13), seasons))
dg['dtseason'] = dg['registration_datetime'].dt.month.map(month_to_season)

# df['day_of_week'] = df['registration_datetime'].dt.day_name()
# dg['hourofweek'] = dg.apply(lambda x:"%02d%02d" % (x['dtweekday'],x['dthour']),axis=1)
dg['hourofweek'] = dg.apply(lambda x: (
    x['dtweekday'] * 24 + x['dthour']), axis=1)


dm = dg.groupby(dg.hourofweek).mean()


# df[['registration_datetime','patient']].resample('60min', on='registration_datetime').apply(countLines)
# plot([1, 2, 3], [1, 2, 3], 'go-', label='line 1', linewidth=2)
dg.set_index(['registration_datetime'], inplace=True)

# Plot the resamle
# data = [go.Scatter(x=da['registration_datetime'], y=dg['patient'])]
# py.iplot(data, filename='time-series-simple')

# spikes = dg.loc[(dg['patient'] >= dg.mean()['patient'] + 2 * dg.std()['patient'] )=
dg['spikes'] = (dg['patient'] >= dg.mean()[
                'patient'] + 2 * dg.std()['patient'])

# Count number of spikes
# dg.groupby([dg.spikes]).count()

############################# End Group by Day/Hour  #############################


da = df[['registration_datetime', 'discharge_datetime', 'patient', ]].copy()

# Iterate through each row and search for the items that are
# in proximity by using a date ran

da.set_index(['registration_datetime'], inplace=True)

if 1 == 0:
    dvisitors = pd.read_csv('Results/DVWithVititsInHour.csv',
                            low_memory=False)

else:

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
        startdate = eventdate

        # startdate = pd.to_datetime('2018-06-28 01:38:08')
        enddate = pd.to_datetime(row['discharge_datetime'])
        # df = df.set_index(['registration_datetime'])

        # print(rowcount, startdate, enddate, index, row['patient'], len(
        #     da.loc[str(startdate):str(enddate)]))
        # print(da.loc[str(startdate):str(enddate)])

        visitorCount[rowcount] = len(
            da.loc[str(startdate):str(enddate)])

        visitorCount[rowcount] = len(
            da.loc[str(startdate):str(enddate)])

        rowcount += 1

    df['visits_within_hour'] = visitorCount
    # df.to_csv('Results/DVWithVititsInHour.csv')
    # df.to_csv('Results/DVWithArrivalsBeforeDischarge.csv')

    df['arrivalsBeforeDischarge'] = visitorCount

spikes = df.loc[(df['visits_within_hour'] >= df.mean()[
    'visits_within_hour'] + 2 * df.std()['visits_within_hour'])]

df[['visits_within_hour', 'patient']].groupby('visits_within_hour').count()


a = df['visits_within_hour'].values.tolist()

# py.iplot(ff.create_distplot([a[c] for c in a.columns], a.columns, bin_size=1),
#          filename='distplot with pandas')


def factorAnalysis(df):
    df.drop(['case', 'patient', 'traige_datetime',
             'discharge_datetime', 'closing_of_ed_record_datetime',
             'arrival_at_department_datetime', 'actual_transfer_datetime',
             'nursing_care_report_start_of_reporting_datetime',
             'movment_reason_1st_and_2nd', 'referrer', 'triage_scale',
             'discharge_from_ed', 'hospitalization',
             'receivement_approvement_of_first_sampling', 'ed_record_creation_date',
             'ed_record_creation_hour', 'hospitalization_department',
             'planned_transfer_date', 'planned_transfer_hour',
             'minutes_from_admittance_to_hospitalization_decision',
             'minutes_from_decision_to_arrival_at_hospitalization_department',
             'summary', 'patient_condition_in_release', 'treatment_recommendation',
             'physical_condition', 'eeg'], axis=1, inplace=True)
    chi_square_value, p_value = calculate_bartlett_sphericity(df)

# dn.drop(['last_results_document_creation_hour','registration_datetime'],axis=1, inplace=True)


# begin example
x = np.random.randn(1000)
hist_data = [x]
group_labels = ['distplot']

fig = ff.create_distplot(hist_data, group_labels)
py.iplot(fig, filename='Basic Distplot')
# End Example

data = [go.Scatter(x=df['registration_datetime'], y=df['visits_within_hour'])]
# data = [go.Scatter(x=dff['registration_datetime'], y=dff['visits_within_hour'])]

py.iplot(data, filename='time-series-simple')

if 1 == 0:
    df.corr().to_csv('Results/Correlation With VisitsWithinHour.csv')


# Reasons people left
df[df.triage_urgency == 1].groupby(['discharge_type']).count()
