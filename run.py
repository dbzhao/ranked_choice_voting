#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 12:59:26 2019

@author: daniel.zhao
"""

import argparse
import logging
import pandas as pd
import sys

from datetime import datetime

from rcv_utilities import *

def main(args):
    """ Run elections from votes.csv
    """
    # Read in csv, load top two rows as multiindex column
    votes = pd.read_csv(args['filename'])

    # If single election provided and matches, then only evaluate that election.
    elections = votes['election'].unique()
    if args['election'] in elections:
        elections = [args['election']]

    # Evaluate each election
    for election in elections:
        logger.warning('Initializing election {}'.format(election))
        winner = run_election(votes[votes['election']==election])
        logger.warning('Election complete: {winner} declared winner for {election}'.format(winner=winner,election=election))
        
    return

# The parser is only called if this script is called as a script/executable (via command line) but not when imported by another script
if __name__=='__main__':
    if len(sys.argv) < 2:
        print "You haven't specified any arguments. Use -h to get more details on how to use this command."
        sys.exit(1)
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="""
        Take csv of votes and evaluate winner based on ranked choice voting method.
        """)
    parser.add_argument('--filename', '-f', type=str, default="votes.csv", help='Filename for votes csv')
    parser.add_argument('--election', '-e', type=str, default=None, help='[OPTIONAL] Single election from data to run')
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Print more while running")

    args = parser.parse_args()

    # Initialize logger
    if args.verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(level=level,
                        filename='election_log_{}.log'.format(datetime.today().strftime('%Y%m%d_%H%M%S')),
                        format="%(asctime)s | %(levelname)-5.5s | %(message)s",
                        handlers=logging.StreamHandler())

    logger = logging.getLogger()

    main(vars(args))
