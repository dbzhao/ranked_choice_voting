import argparse
import logging
import pandas as pd
import sys
import time

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
        print ''

        # If not, iterate through candidates until winner is found
        while has_winner == False:
            # TODO: Log this
            loser = rce.get_loser(tally)
            last_tally = tally

            # Remove candidate
            rce.remove_candidate(rce.votes, loser)
            print 'Last place candidate {loser} eliminated with {votes:.0f} votes'.format(loser=loser, votes=tally.ix[loser]['First Choice'])

            tally = rce.tally_votes(rce.votes, rce.candidates)

            # Compare against last round
            comp_df = pd.merge(tally, last_tally, left_index=True, right_index=True, suffixes=[' Current', ' Previous'])
            comp_df['First Choice Diff'] = comp_df['First Choice Current'] - comp_df['First Choice Previous']
            changes = comp_df[comp_df['First Choice Diff']>0]['First Choice Diff'].astype(int)

            if len(changes) > 0:
                print 'Votes distributed to remaining candidates:'
                for i in changes.index:
                    print ' * {num_votes} votes distributed to {candidate}'.format(num_votes=changes.ix[i], candidate=i)

            print ''
            # TODO: Write logs to file

            has_winner, winner = rce.get_winner(tally)

        print '...'
        print 'The winner for election {question} is {winner} with {votes:.0f} votes'.format(question=question,
                                       winner=winner,
                                       votes=int(tally['First Choice'].ix[winner]))


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

    args = parser.parse_args()

    main(vars(args))
