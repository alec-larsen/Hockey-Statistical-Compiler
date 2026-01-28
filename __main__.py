import time
import traceback
from validation.connection import verify_connection_codes
from validation.verification_error import VerificationError

from benchmark import benchmark_ingestion
from core import display

try:
    #Before model runs, verify local system is configured to properly run this program.
    verify_connection_codes() #System fetches correct status codes from get calls.
    display.print_banner("Welcome to AneStat")

    while True:
        choice = display.get_menu_option()
        if choice == "1":
            n,t = benchmark_ingestion.benchmark_ingestion()
            print(f"{n} play-by-plays successfully ingested from NHL API in {t:.3f} seconds")

        elif choice == "2":
            t = benchmark_ingestion.benchmark_clean_all()
            print(f"All data on system cleaned in {t:.3f} seconds.")

        elif choice == "3":
            print("-"*60 + "\n" + "ANESTAT SESSION CLOSED: TERMINATING IN 3 SECONDS\n" + "-"*60)
            time.sleep(3)
            break

        else:
            display.print_banner("INVALID COMMAND INPUT: PLEASE INPUT VALID OPTION")

except VerificationError as ve:
    print(f"\033[91m{ve.__class__.__name__}: {ve}\033[0m")
    input("Please press 'Enter' to exit...")

except Exception as e: #pylint: disable=broad-exception-caught
    print(f"\033[91m{''.join(traceback.format_exception(e))}\033[0m")
    input("Please press 'Enter' to exit...")
