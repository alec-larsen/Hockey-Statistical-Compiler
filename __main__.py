import time
import traceback
from validation.connection import verify_connection_codes
from validation.presence import verify_raw_data
from validation.exceptions import VerificationError, NetworkError, ExcessDelayError

from benchmark import benchmark_ingestion
from core import display

try:
    display.print_banner("WELCOME TO ANESTAT 0.1.0")

    while True:
        #Ask for another user input for next menu option.
        choice = display.get_menu_option()

        #Choosing '1' ingests the next 100 required raw play-by-plays from the NHL API.
        #If less than 100 remain to ingest, we just ingest all remaining required data.
        if choice == "1":
            display.print_banner("INGESTION: VERIFYING CONNECTION")
            #Check that system fetches correct status codes from get calls.
            verify_connection_codes()
            n,t,all_ingested = benchmark_ingestion.benchmark_ingestion()
            print(f"{n} play-by-plays successfully ingested from NHL API in {t:.3f} seconds")

            if all_ingested:
                verify_raw_data()

        #Choosing '2' cleans all raw data present in data/raw/
        #Previously cleaned data will be overwritten
        elif choice == "2":
            display.print_banner("CLEANING: CLEANING ALL RAW DATA")
            t = benchmark_ingestion.benchmark_clean_all()
            print(f"All data on system cleaned in {t:.3f} seconds.")

        #Choosing '3' exits the program.
        elif choice == "3":
            print("-"*60 + "\n" + "ANESTAT SESSION CLOSED: TERMINATING IN 3 SECONDS\n" + "-"*60)
            time.sleep(3)
            break

        #Any other input will not be accepted
        else:
            display.print_banner("INVALID COMMAND INPUT: PLEASE INPUT VALID OPTION")

        display.print_banner("CURRENT PROCESS COMPLETED: AWAITING NEXT COMMAND")

#Catch any errors specifically flagged as verification-related.
#These should not be code-related, but indicative of a local issue (e.g. missing data, network issues)
except (VerificationError, NetworkError, ExcessDelayError) as ve:
    print(f"\033[91m{ve.__class__.__name__}: {ve}\033[0m")
    input("Please press 'Enter' to exit...")

#Any unexpected errors should return a full stacktrace.
except Exception as e: #pylint: disable=broad-exception-caught
    print(f"\033[91m{''.join(traceback.format_exception(e))}\033[0m")
    input("Please press 'Enter' to exit...")
