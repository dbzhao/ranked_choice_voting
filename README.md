# ranked_choice_voting
Implement ranked choice voting evaluation for GD Hacks.

## Usage Instructions
1. Parse data into specified format:
```
respondent_id | election | rank | vote
123456        | award1   | 1    | team_a
123456        | award1   | 2    | team_b
123456        | award1   | 3    | team_c
123456        | award2   | 1    | team_d
...
```

For our SurveyMonkey poll, results can be reformated properly using `load_data_hack14.py`. **Note:** The code is pretty brittle as it requires the votes to be in a particular format and SurveyMonkey changes their output formats somewhat often.

2. Run from command line `python run.py -f "votes.csv" -v`. This will evaluate an election for every election present in the dataset. `-v` flag specifies verbose and adds detail to the log file for debugging.
