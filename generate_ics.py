from yahoo_earnings_calendar import YahooEarningsCalendar  # earnings calendar API for us to filter through
import ics # for creating the ICS file
import datetime
from os import path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f",  "--input-file", help="location of the input file")
parser.add_argument("-o", "--output-file", help="location of the generated output file", default="next_earnings_calendar.ics")
args = parser.parse_args()
output_file = args.output_file
input_filename = args.input_file

def create_ics(output_filename, input_filename=None):
    output_calendar = ics.Calendar(creator="Earnings Calendar Invites")
    yec = YahooEarningsCalendar()
    added_stocks = []
    if(input_filename != None):
        file_ptr = open(file=input_filename, mode="r")
    while True:
        ### Stock selection
        if(input_filename != None):
            stock_name = file_ptr.readline().strip()
            if(len(stock_name) == 0):
                print(f"Finished selecting {len(added_stocks)} stocks, outputting ICS.")
                file_ptr.close()
                break
        else:
            stock_name = str(input("Enter stock ticker (type \'done\' to finish inputting tickers): "))
            if(stock_name == 'done'):
                print(f"Finished selecting {len(added_stocks)} stocks, outputting ICS.")
                break

        ### Getting the earnings date information and adding it to the calendar
        if (stock_name) not in added_stocks:
            next_earnings_unix = 0;
            try:
                ### Getting the information
                next_earnings_unix = int(yec.get_next_earnings_date(stock_name))
            except Exception as e:
                print(e)
            else:
                ### Extracting earnings date and reformatting for usage
                earnings_date = datetime.datetime.utcfromtimestamp(next_earnings_unix).strftime('%Y-%m-%d %H:%M:%S')
                ics_earnings_date = datetime.datetime.strptime(earnings_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                human_earnings_date = datetime.datetime.strptime(earnings_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
                
                ### Deciding if it should be added to the calendar
                add_to_calendar = str(input(f"Earnings date for {stock_name} found ({human_earnings_date}). Add to calendar (default Y)? [Y/n]: ") or "Y")
                if(add_to_calendar.lower() == "y"):
                    e = ics.Event(name=f"{stock_name} earnings", begin=ics_earnings_date)
                    e.make_all_day()
                    output_calendar.events.add(e)
                    added_stocks.append(stock_name)
                    print("Added to calendar.")
                else:
                    print("Not added.")
        else:
            print(f"{stock_name} has already been added to the calendar")
        print() # makes the print a little easier on the eyes

    if(len(added_stocks) != 0):
        with open(output_filename, mode="w") as output_file:
            output_file.writelines(output_calendar)
            print(f"{output_filename} created with {len(added_stocks)} earnings dates.")
    else:
        print("No stocks were added to the calendar so no earnings calendar was created.")


if __name__ == "__main__":
    if(args.input_file is not None):
        if(path.exists(args.input_file) and path.isfile(args.input_file)):
            create_ics(output_filename=args.output_file, input_filename=args.input_file)
        else:
            print(f"File {args.input_file} does not exist. Entering console interactive mode.")
            create_ics(output_filename=args.output_file)
    else:
        print(f"You didn't specify a input file. Entering console interactive mode.")
        create_ics(output_filename=args.output_file)
