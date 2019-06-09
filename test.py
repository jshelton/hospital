#!/usr/bin/python
from datetime import timedelta

from dateutil import parser

import csv


class Counter(object):
    wheels = 0
#    def __init__(self, other):
#          self.make = other

    def count(self):
        self.wheels += 1
        return str(self.wheels)


with open('Data/ERlast2years.csv') as csvfile:
    reader = csv.DictReader(csvfile)

#
    row1 = next(reader)
    row2 = next(reader)
    row = row2
#	asize = 0
#	for row in reader:
#	print(row.keys().join(','))

    mycounter = Counter()

    # print(mycounter.count())
    # print(mycounter.count())
    # print(mycounter.count())

    print('\n '.join("%s=%r" % (mycounter.count() + " " + key, val)
                     for (key, val) in row.items()))
#	print(parser.parse(row['discharge_datetime'])-parser.parse(row['registration_datetime']))
#	print(parser.parse(row2['registration_datetime'])-parser.parse(row1['registration_datetime']))

# discharge_datetime
# registration_datetime
# receivement_approvement_of_first_sampling
# minutes_from_admittance_to_discharge
# last_results_document_creation_hour


#	asize = asize + 1
#	print(asize)
    # size = 5
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
#             print row[0]
#             print(parser.parse(row[0]['registration_datetime']) -
#                   parser.parse(row[1]['registration_datetime']))

#             row[0] = row[1]
