import argparse
import logging
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
    questions, candidates, votes = load_data.parse_questions_candidates_votes()

    # Evaluate each election
    for question in questions:
        rce = election.RankedChoiceElection(votes[question], candidates)

        # Tally and check for winner
        tally = rce.tally_votes(rce.candidates, rce.votes)
        has_winner, winner = rce.get_winner(tally)

        # If not, iterate through candidates until winner is found
        while has_winner == False:
            # Log this
            loser = rce.get_loser(new_tally)
            rce.remove_candidate(rce.votes, loser)

            tally = rce.tally_votes(rce.candidates, rce.votes)
            has_winner, winner = rce.get_winner(tally)

            # TODO: Write logs to txt?


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

    args = parser.parse_args()

    main(vars(args))
