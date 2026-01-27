import timeit
import os

from core.constants import ROOT_DIRECTORY

def benchmark_ingestion() -> tuple[int,float]:
    """
    Obtain total time for ingestion of 100 play-by-plays, at least 100 are required to write.
    
    If there are less than 100 play-by-plays remaining to write, obtain total time to ingest all
    remaining play-by-plays.
    
    Returns:
        int: Number of play-by-plays written.
        float: Total time taken to ingest 100 play-by-plays.
    """
    setup = "from core.ingestion import write_next_pbp"
    ingest = "write_next_pbp()"

    current_files = os.listdir(ROOT_DIRECTORY / "data" / "raw")

    #If there are less than 100 remaining play-by-plays to ingest, write all remaining data.
    #Subtract 1 from number of raw data files to account for .gitkeep in data/raw/
    n = min(len(current_files)-1, 100)

    #Get time (in seconds) for set of ingestion calls
    t = timeit.timeit(stmt = ingest, setup = setup, number = n)
    return (n,t)

def benchmark_clean_all(rep: int = 1) -> float:
    """
    Obtain total time for cleaning all raw data currently on system.

    Args:
        rep (int): Number of repetitions of cleaning cycle to average over (defaults to 1)
        
    Returns:
        float: Average time taken to clean all raw play-by-play data in local system
    """
    setup = "from core.ingestion import clean_all_pbp"
    clean = "clean_all_pbp()"

    #Get time (in seconds) for [rep] calls of this function.
    t = timeit.timeit(stmt = clean, setup = setup, number = rep)
    return t/rep
