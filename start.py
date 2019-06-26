from pandas import DataFrame
from pylab import rcParams
import matplotlib
import statsmodels.api as sm
import itertools
import warnings
import csv
from dateutil import parser
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity


import numpy as np
import time
import hebcal

from sklearn.linear_model import LinearRegression


import pandas as pd
from datetime import datetime, timedelta


warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'


fileName = 'Data/ERlast2years.csv'


parse_dates = ['registration_datetime', 'traige_datetime', 'discharge_datetime', 'closing_of_ed_record_datetime', 'arrival_at_department_datetime',
               'actual_transfer_datetime', 'nursing_care_report_start_of_reporting_datetime', 'receivement_approvement_of_first_sampling', 'last_results_document_creation_hour']

# dtype={"hospitalization_department": str, "planned_transfer_date": str, "minutes_from_admittance_to_discharge": str, "referrer": str, "triage_urgency": int32)

start = time.time()

df = pd.read_csv(fileName,
                 parse_dates=parse_dates, low_memory=False)

end = time.time()
print("Imported CSV: ", end - start)


df = df.sort_values('registration_datetime')

# Prepare Dataframe for working with data

df['hour'] = df['registration_datetime'].dt.hour
df['month'] = df['registration_datetime'].dt.month
df['day'] = df['registration_datetime'].dt.day
df['weekday'] = df['registration_datetime'].dt.weekday

# This has monday = 0

seasons = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 1]
month_to_season = dict(zip(range(1, 13), seasons))
df['season'] = df['registration_datetime'].dt.month.map(month_to_season)
df['hourofweek'] = df.apply(lambda x: "%02d%02d" %
                            (x['weekday'], x['hour']), axis=1)

df['registrationFloor'] = df['registration_datetime'].dt.floor("H")
df['countItems'] = 1

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


dg = df[['registration_datetime', 'countItems', 'minutes_from_admittance_to_discharge']].resample(
    '60min', on='registration_datetime').sum()

dg = df[['registration_datetime', 'countItems', 'minutes_from_admittance_to_discharge']].resample(
    '60min', on='registration_datetime').sum()


# dg.set_index(['registration_datetime'], inplace=True)

dg['registration_datetime'] = dg.index

dd['registration_datetime'] = dd.index

# plt.scatter(dg['registration_datetime'], dg['countItems'])


y = dg['countItems']

rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(y, model='additive')
# fig = decomposition.plot()

# print(decomposition.trend)
# print(decomposition.seasonal)
# print(decomposition.resid)
# print(decomposition.observed)

dg['stabalized'] = decomposition.resid


dg['delta'] = dg['stabalized'].diff()

# plt.scatter(dg['registration_datetime'], dg['delta'])


# dg.dropna(inplace=True)

dg['deltapositive'] = dg.apply(
    lambda row: 1 if row['delta'] > 0 else 0, axis=1)

# dg['deltapositivetrend'] = dg.apply(
#     lambda row: 1 + row['deltapositive'].shift() if row['delta'] > 0 else 0)

dg['spike'] = (dg['stabalized'] >= dg.mean()[
    'stabalized'] + 2 * dg.std()['stabalized'])

# plt.scatter(dg['registration_datetime'], dg['spike'])

# Count number of spikes
# dg.groupby([dg.spikes]).count()

############################# End Group by Day/Hour  #############################

# start = time.time()
# df['spikeStdDev'] = df.apply(
#     lambda row: dg.loc[df['registration_datetime'].dt.floor("H")]['spike'], axis=1)


# end = time.time()
# print("Spikes due to statistical impressoin", end - start)


# start = time.time()

# df['visitsInHour'] = df.apply(lambda row: len(da.loc[str(
#     pd.to_datetime(row['registration_datetime'])
# ):str(pd.to_datetime(row['discharge_datetime']))]), axis=1)
# end = time.time()
# print("Spike: visitors in hour", end - start)


da = df[['registration_datetime', 'discharge_datetime', 'patient', ]].copy()

# Iterate through each row and search for the items that are
# in proximity by using a date ran

df.set_index(['registration_datetime'], inplace=True)


# if 1 == 0:
#     dvisitors = pd.read_csv('Results/DVWithVititsInHour.csv',
#                             low_memory=False)
# else:
visitorCount = np.zeros(len(df))
spikesHour = np.zeros(len(df))

maxCount = 300
limitRuns = False

start = time.time()
rowcount = 0
for index, row in df.iterrows():
    rowcount += 1
    if (rowcount % 2500 == 0):
        end = time.time()
        print(end - start, rowcount)
        start = time.time()

        if limitRuns and rowcount > maxCount:
            break

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
        df.loc[str(startdate):str(enddate)])

    lookupTime = pd.to_datetime(index).floor("H")
    spikesHour[rowcount] = dg.loc[lookupTime]['spike']

df['visits_within_hour'] = visitorCount
df['spikesHour'] = spikesHour
# df.to_csv('Results/DFSpikesVisits.csv')
# df.to_csv('Results/DVWithVititsInHour.csv')
writeToFiles = True
if 1 == 0:
    df.corr().to_csv('Results/Correlation With VisitsWithinHour.csv')
    df.to_csv('Results/DFCorrelations.csv')


############
# What time do people go in a week
ct.pd.crosstab(index=df["age"],
               columns=df["hourofweek"])

# heatmap


plt.pcolor(ct)
# plt.yticks(np.arange(0.5, len(ct.index), 1), ct.index)
# plt.xticks(np.arange(0.5, len(ct.columns), 1), ct.columns)
plt.show()


spikes = df.loc[(df['visits_within_hour'] >= df.mean()[
    'visits_within_hour'] + 2 * df.std()['visits_within_hour'])]

df[['visits_within_hour', 'patient']].groupby('visits_within_hour').count()


a = df['visits_within_hour'].values.tolist()

# py.iplot(ff.create_distplot([a[c] for c in a.columns], a.columns, bin_size=1),
#          filename='distplot with pandas')

dm = dg.copy()

# def factorAnalysis(df):
dm.drop(['case', 'patient', 'traige_datetime',
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
         'physical_condition', 'eeg', 'registration_datetime'], axis=1, inplace=True)
chi_square_value, p_value = calculate_bartlett_sphericity(dm)

# dn.drop(['last_results_document_creation_hour','registration_datetime'],axis=1, inplace=True)


fa = FactorAnalyzer()
fa.analyze(dm, 25, rotation=None)


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


# Reasons people left
df[df.triage_urgency == 1].groupby(['discharge_type']).count()


agesCount = df['countItems'].groupby(df.age).count()
agesCount.hist(bins=100)
