import pandas as pd
import numpy as np
import datetime

analysisDate = datetime.datetime(2017,3,1)
cutoffDate = datetime.datetime(2017,2,15)

#read employee data source 1
employee1 = pd.read_csv('Employee1.csv')
employee1 = employee1.loc[employee1['Report Dt'] == '3/31/2017']

# read employee data source 2
employee2 = pd.read_csv('Employee2.csv')
employee2 = employee2.loc[employee2['Report Dt'] == '3/31/2017']

# concatenate employee data sources into one dataframe
employees = pd.concat([employee1, employee2])

# read event data
events = pd.read_csv('Event.csv')

# scrub all rows where Employee ID is null
events = events[pd.notnull(events['Employee ID'])]

# change all Employee ID values from float to int
events["Employee ID"] = events["Employee ID"].astype(int)

def calculate_hours(employeeID):
    temp = events.loc[events['Employee ID'] == employeeID]
    temp = temp.loc[pd.to_datetime(temp['Begin Date']) > cutoffDate]
    temp = temp.loc[pd.to_datetime(temp['Begin Date']) < analysisDate]
    return temp['Total Recorded'].sum()

# aggregate hours worked in the month prior to the analysis
hoursWorked = [0] * employees.shape[0]
i = 0
for index, row in employees.iterrows():
    employeeID = row['Employee Number']
    hours = calculate_hours(employeeID)
    row["hoursWorked"] = hours
    hoursWorked[i] = hours
    i = i + 1

# append new feature column to dataframe
employees["hoursWorked"] = hoursWorked

# write dataframe to csv
employees.to_csv('employee_data.csv')
