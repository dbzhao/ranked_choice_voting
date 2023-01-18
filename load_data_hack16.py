#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 20:07:26 2020

@author: daniel.zhao
"""

import pandas as pd

FILENAME = "Hack 19 Award Survey.csv" # Downloading from SurveyMonkey breaks the spaces in the filename

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
#df.drop(df.columns[-12:], axis=1, inplace=True) # Drop extra questions

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
