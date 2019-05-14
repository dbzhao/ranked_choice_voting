import argparse
import logging
import numpy as np
import pandas as pd
import sys

import election
import load_data


def main(args):

    # Read in csv
    df = pd.read_csv(args['filename'])

    # Clean out any duplicates
    df = load_data.check_duplicates(df, keep='last')

    # Parse out questions, candidates and votes
    questions, candidates, votes = load_data.parse_questions_candidates_votes(df)

    # If single election provided and matches, then only evaluate that election.
    if args['election'] in questions:
        questions = [args['election']]

    # Evaluate each election
    for question in questions:
        rce = election.RankedChoiceElection(votes[question], candidates)

        # Tally and check for winner
        tally = rce.tally_votes(rce.votes, rce.candidates)
        has_winner, winner = rce.get_winner(tally)

        # If not, iterate through candidates until winner is found
        while has_winner == False:
            logger.info('No winner found')
            loser = rce.get_loser(tally)
            last_tally = tally

            # Remove candidate
            rce.remove_candidate(rce.votes, loser)
            logger.info('Last place candidate {loser} eliminated with {votes:.0f} votes'.format(loser=loser, votes=tally.ix[loser]['First Choice']))

            tally = rce.tally_votes(rce.votes, rce.candidates)

            # Compare against last round
            comp_df = pd.merge(tally, last_tally, left_index=True, right_index=True, suffixes=[' Current', ' Previous'])
            comp_df['First Choice Diff'] = comp_df['First Choice Current'] - comp_df['First Choice Previous']
            changes = comp_df[comp_df['First Choice Diff']>0]['First Choice Diff'].astype(int)

            if len(changes) > 0:
                logger.info('Votes distributed to remaining candidates:')
                for i in changes.index:
                    logger.info(' * {num_votes} votes distributed to {candidate}'.format(num_votes=changes.ix[i], candidate=i))

            # TODO: Write logs to file

            has_winner, winner = rce.get_winner(tally)

        # TODO: also print # of ballots

        logger.warning('Out of {} ballots cast:'.format(len(votes[question])))
        logger.warning('Winner found')
        logger.warning('The winner for election {question} is {winner} with {votes:.0f} votes'.format(question=question,
            winner=winner,
            votes=int(tally['First Choice'].ix[winner])))
        
        # Print 1st-3rd place
        logger.warning(tally['First Choice'][0:3].sort_values(ascending=False))

# The parser is only called if this script is called as a script/executable (via command line) but not when imported by another script
if __name__=='__main__':
    if len(sys.argv) < 2:
        print "You haven't specified any arguments. Use -h to get more details on how to use this command."
        sys.exit(1)
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="""
        Take csv of votes and evaluate winner based on ranked choice voting method.
        """)
    parser.add_argument('--filename', '-f', type=str, default=None, help='Filename for votes csv')
    parser.add_argument('--election', '-e', type=str, default=None, help='[OPTIONAL] Single election from data to run')
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Print more while running")

    args = parser.parse_args()

    # Initialize logger
    if args.verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(level=level,
        format="%(asctime)s | %(levelname)-5.5s | %(message)s",
        handlers=logging.StreamHandler())

    logger = logging.getLogger()

    main(vars(args))
