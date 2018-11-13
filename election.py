import logging
import pandas as pd
import re

class RankedChoiceElection:

    vote_map = {'First Choice': 1, 'Second Choice': 2, 'Third Choice': 3}
    rank_map = {1: 'First Choice', 2: 'Second Choice', 3: 'Third Choice'}

    def __init__(self, votes, candidates):
        self.votes = votes
        self.candidates = candidates


    def tally_votes(votes, candidates):

        tallied = pd.DataFrame(columns=['First Choice', 'Second Choice', 'Third Choice'])

        for candidate in candidates:
            candidate_column = [column for column in votes.columns if re.search(candidate, column)][0]
            vote_counts = votes[candidate_column].value_counts()
            vote_counts = pd.DataFrame(vote_counts).transpose()
            tallied = pd.concat([tallied, vote_counts])
            tallied = tallied.fillna(0.0)

        return tallied


    def get_winner(df):
        total_votes = df['First Choice'].sum()
        if total_votes == 0:
            print 'Not enough votes'
            return (False, '')
        elif max(df['First Choice']) >= (total_votes / 2) + 1:
            print 'Winner found'
            return (True, df['First Choice'].idxmax())
        else:
            print 'No winner found'
            return (False, '')


    def get_loser(df):
        # Return loser, ties broken by random shuffling based on random_state=1
        # TODO: Add logging for tiebreaks
        return df[df['First Choice']==min(df['First Choice'])].sample(frac=1, random_state=1).index[0]


    def remove_candidate(df, candidate_column):

        new_votes = pd.DataFrame()

        for i in df.index:
            id_row = df.ix[i][['Timestamp', 'Email Address']]
            vote_row = df.ix[i][~df.columns.isin(['Timestamp', 'Email Address'])].drop(candidate_column)
            vote_row = vote_row.map(vote_map)
            vote_row = vote_row.rank() # TODO: Add logging for who votes have been redistributed to
            vote_row = vote_row.map(rank_map)
            vote_row = pd.concat([id_row, vote_row])
            new_votes = pd.concat([new_votes, pd.DataFrame(vote_row).transpose()])

        candidate = re.findall('\[(.+)\]', candidate_column)[0]

        if candidate in self.candidates:
            self.candidates.remove(candidate)

        return new_votes
