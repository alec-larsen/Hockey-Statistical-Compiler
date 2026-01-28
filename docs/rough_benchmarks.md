# Rough Time Benchmarks
As my model continues to progess, I will make my best effort to track how fast my model runs its key steps.

## Ingestion
Due to rate-limiting on the NHL API, I tend to ingest all required data for the model in batches of 100 games with a time of no less than 1 hour between batch collections. Currently, I have obtained the following runtimes for each batch of 100 play-by-plays ingested:

- 2024 (1-100): 28.235 seconds
- 2024 (101-200): 28.158 seconds
- 2024 (201-300): 30.463 seconds
- 2024 (301-400): 29.936 seconds
- 2024 (401-500): 30.583 seconds

Based on the above runtimes, the model takes, on average, about 0.295 seconds to ingest one play-by-play directly from the NHL API.

## Cleaning/Compression
Cleaning the data is done post-ingestion, so, if done from raw data, the entire dataset can be cleaned in one pass.

I have now implemented a function that cleans all raw data, regardless of whether it has already been cleaned. Recent calls to cleaning have yielded results as follows:

- 2024 (1-500): 9.149 seconds

Based on the above runtimes, the model takes, on average, about 0.018 seconds to clean each play-by-play from the raw data.

## Breakdown of Overall Pipeline Time (So Far)
1. **Ingestion**
    
    As a season has 1312 total regular season games, we should expect one season to take about:
    
    $$1312gm*0.295s/gm \approx 387s$$

    6m 27s to fully ingest.
    
    Unfortunately, due to rate limiting on the NHL API, an entire season cannot be collected in one pass. As such, the actual time to get all data fully ingested is much longer.

2. **Cleaning/Compression**

    Doing the same calculation as we did above with ingestion, we find that, for an entire season of play-by-plays, the model takes:

    $$1312gm*0.018s/gm \approx 23.6s$$

    less than 25 seconds to clean and compress the raw data into a more usable format.