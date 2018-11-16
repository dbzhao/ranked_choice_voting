import logging
import pandas as pd
import re

def check_duplicates(df, keep=False):

    df.sort_values(by='Timestamp', ascending=True, inplace=True)

    # Setting keep_invalid to False will drop all duplicated records, 'last' will preserve only last record
    df = df[~df['Email Address'].duplicated(keep=keep)]

    # TODO: Log whether there are any duplicates and who the offenders are

    return df

def parse_questions_candidates_votes(df):
    questions_and_candidates = list(df.columns[2:])

    questions = list(pd.unique([re.findall('(.+)\[', i)[0].strip() for i in questions_and_candidates]))
    candidates = list(pd.unique([re.findall('\[(.+)\]', i)[0].strip() for i in questions_and_candidates]))

    votes = {}

    for question in questions:
        question_columns = [column for column in df.columns if re.search(question, column)]
        votes[question] = df[['Timestamp', 'Email Address'] + question_columns]

    # TODO: Log the questions and candidates

    return questions, candidates, votes
