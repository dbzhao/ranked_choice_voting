#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 20:07:26 2020

@author: daniel.zhao
"""

# Now from Google Sheets

import numpy as np
import pandas as pd

FILENAME = "Hack 20 Awards Survey.csv" 

# Load data from CSV
df = pd.read_csv(FILENAME)

# Get all vote columns with colons
df = df.loc[:,df.columns[df.columns.str.contains(':')]]

# Split columns into multiindex to split elections and teams into diff levels
idx = df.columns.str.split('[', expand=True)
df.columns = idx

df = df.reset_index()

# Convert df from long to wide
votes = df.melt(id_vars=['index']).dropna()
votes['election'] = votes['variable_0'].apply(lambda x: x.split(':')[0])

# Collapse multivotes to highest rank vote
choice_map = {'First Choice': '1', 'Second Choice': '2', 'Third Choice': '3'}
votes['rank'] = votes['value'].replace(choice_map, regex=True)
votes['rank'] = votes['rank'].apply(lambda x: min(x.split(';'))).astype('int')

# Clean up columns/data
votes['vote'] = votes['variable_1'].str.replace(']', '', regex=False)
votes.rename(columns={'index': 'respondent_id'}, inplace=True)

# Filter just to relevant columns
votes = votes[['respondent_id', 'election', 'rank', 'vote']]

# Final output should be respondent_id, election, rank, vote as cols

# Write final output out to CSV
votes.to_csv('votes.csv', header=True, index=False)
