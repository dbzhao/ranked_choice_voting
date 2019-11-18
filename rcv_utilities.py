#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Utility functions to run ranked choice vote election

Created on Mon Nov 18 13:02:06 2019

@author: daniel.zhao
"""

import logging
import pandas as pd
import sys


def tally_votes(votes, candidates):
    """Tally first-choice votes and readd any candidates w/ 0 first choices"""
    nonzeroes = votes[votes['rank']==1].groupby('vote')['respondent_id'].count()
    index = pd.DataFrame(candidates, columns=['candidate'])

    output = pd.merge(left=index,
                      right=nonzeroes,
                      how='left',
                      left_on='candidate',
                      right_index=True
                      )
    
    output = output.set_index('candidate')
    output = output.fillna(0)
    output = output.astype('float')

    return output['respondent_id']

def get_winner(tally):
    """Declare winner from vote tally if candidate has vote majority"""
    if tally.sum() == 0:
        sys.exit('Not enough votes')
        return (False, None)
    elif tally.max() > tally.sum()/2:
        return (True, tally.idxmax())
    else:
        return (False, None)

def get_loser(tally):
    """Declare loser from vote tally as candidate with fewest votes. Ties
        broken randomly. Random state forced to 1 for replicability.
    """
    return tally.sample(frac=1, random_state=1).idxmin()

def remove_candidate(votes, candidate):
    """Remove given candidate from votes"""
    new_votes = votes[votes['vote']!=candidate]
    new_votes = densify_ranks(new_votes)
    return new_votes

def densify_ranks(df, id_col='respondent_id'):
    """Densify rank data to remove gaps in ranks"""
    # Make sure sorted
    df.sort_values(by=id_col, ascending=True)
    
    # Densify rank skipping gaps, should never tie
    df.loc[:,'rank'] = df.groupby(id_col)['rank'].rank().astype('int')
    
    return df

def run_election(votes):
    """Run election"""
    
    # Get logger from above
    logger = logging.getLogger(__name__)
    
    # Initialize while loop
    candidates = votes['vote'].unique()
    tally = tally_votes(votes, candidates)
    logger.info(tally.sort_values(ascending=False))
    has_winner, winner = get_winner(tally)
    
    while has_winner == False:
        # Find & remove loser
        logger.info("No winner found")
        loser = get_loser(tally)
        logger.info("Removing {}".format(loser))
        votes = remove_candidate(votes, loser)
        candidates = votes['vote'].unique()
        
        # Recalculate tally
        tally = tally_votes(votes, candidates)
        logger.info(tally.sort_values(ascending=False))
        
        # Check for winner
        has_winner, winner = get_winner(tally)
    
    logger.warning("Winner declared: {winner} with {num_votes}".format(winner=winner, num_votes=tally.loc[winner]))
    logger.info(tally.sort_values(ascending=False))

    return winner
