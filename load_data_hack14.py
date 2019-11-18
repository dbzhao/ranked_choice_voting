#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Reformat data from SurveyMonkey (as of 2019-11-17) to vote dictionaries

Created on Sun Nov 17 20:56:06 2019

@author: daniel.zhao
"""

import pandas as pd

FILENAME = "Hack 14 Award Survey.csv"

# Load data from CSV
df = pd.read_csv(FILENAME, header=[0,1])

# Get all columns after metadata
last_col = list(df.columns.get_level_values(0)).index('Custom Data 1')

# Crunch columns to single level
new_cols = []
for i in df.columns:
    if 'Unnamed' in i[1]:
        new_cols.append(i[0])
    elif 'Unnamed' in i[0]:
        new_cols.append((last_election, i[1]))
    else:
        tmp = (i[0][0:16], i[1])
        new_cols.append(tmp)
        last_election = tmp[0]

df.columns = new_cols

# Drop metadata columns
df.drop(df.columns[1:last_col+1], axis=1, inplace=True)

# Convert df from long to wide
votes = df.melt(id_vars=['Respondent ID']).dropna()
votes['election'] = votes['variable'].apply(lambda x: x[0])
votes['rank'] = votes['value'].map({'First Choice': 1, 'Second Choice': 2, 'Third Choice': 3})
votes['vote'] = votes['variable'].apply(lambda x: x[1])
votes.rename(columns={'Respondent ID': 'respondent_id'}, inplace=True)

# Filter just to relevant columns
votes = votes[['respondent_id', 'election', 'rank', 'vote']]

# Final output should be respondent_id, election, rank, vote as cols

# Write final output out to CSV
votes.to_csv('votes.csv', header=True, index=False)
