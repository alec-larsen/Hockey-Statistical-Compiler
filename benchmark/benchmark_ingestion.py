import timeit

def benchmark_ingestion() -> None:
    """
    Obtain total time for ingestion of 100 play-by-plays.
    """
    setup = "from core.ingestion import write_next_pbp"
    ingest = "write_next_pbp()"

    #Get time (in seconds) for 100 ingestion calls
    t = timeit.timeit(stmt = ingest, setup = setup, number = 100)
    print(t)

def benchmark_cleaning() -> None:
    """
    Obtain total time for cleaning of 100 play-by-plays (from raw JSONs on local system).
    """
    setup = "from core.ingestion import clean_next_pbp"
    clean = "clean_next_pbp()"

    #Get time (in seconds) for 100 cleaning calls
    t = timeit.timeit(stmt = clean, setup = setup, number = 100)
    print(t)
