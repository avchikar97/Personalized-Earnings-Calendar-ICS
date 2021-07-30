# Personalized-Earnings-Calendar-ICS
Python script to easily create calendar events for the next earnings dates of inputted stock tickers by creating an ICS that can be imported.

### Requirements
- python 3.6 or later (can be installed [here](https://www.python.org/downloads/))
- pip3

### Steps to run:
1. Run `pip3 install -U -r requirements.txt`
2. To use in console input mode:

    2a. Run `python3 generate_ics.py` and follow the prompts
3. To use in file input mode:

    3a. Make sure your input file has the same format as inputs.example.txt (one ticker symbol per line)

    3b. Run `python3 generate_ics.py -f inputs.txt` - the input file may be named anything
4. The output file may be specified with the `-o` parameter (e.g. `python3 generate_ics.py -o output.ics` or `python3 generate_ics.py -f inputs.txt -o output.ics`). The default output file is `next_earnings_calendar.ics`.
