# NHL Statistical Compiler (AneStat v2)
A modular NHL data pipeline built in Python, primarily intended for the ingestion, compilation, and analysis of high volumes of NHL data for playoff and game odds projections.

**Please note: this project is still in very early development.**

## Background
This project is intended to improve on a previous statistical model I have already developed. Though I am fairly proud of my work on AneStat v1, there are several reasons I have chosen to work towards an improvement.

1. **Programming Language:**

    AneStat v1 is almost entirely constructed in R. While I still use R frequently, and intend to incorporate R modules for statistical analysis near the end of the pipeline, it has proven less efficient to rely on for ingestion and processing.
    
    As v1 already relies on Python's sklearn library to build the regression model, running the model primarily through R adds unnecessary overhead. AneStat v2 will eliminate this extra step, saving both time and local resources.

2. **Data Access:**
    
    AneStat v1 was designed to handle a fairly narrow scope of data; only team-level summary statistics for each NHL game. Due to the relatively small volume of data changing within the model daily, no automated ingestion was ever included in the features, with all new data being added manually.
    
    AneStat v2 will be built to automate the ingestion of yesterday's game data, allowing data updates to be completed with a single call. In addition, as v2 can ingest directly from the NHL API, a much larger volume of data is available for use.

    In particular, as opposed to only team-level statistics, v2 will pull play-by-play data from every game in the previous and current NHL regular seasons, allowing for data analysis on the level of individual players.

3. **Coding Practices:**

    AneStat v1 was primarily built for personal use, with both the documentation and general formatting reflecting this fact.
    
    AneStat v2 will be built with three main ideas in mind; efficiency, comprehensibility, and reproducibility.

## Key Features
AneStat v2 is currently in active development as my main priority. The following features have been implemented, or planned

### Currently Implemented

- Early verification checks for proper web connection
- Ingestion of play-by-play data by specific `game_id`
- Compression of raw JSON data; reducing total data size to ~34-35% of initial size.

### Planned
- Compilation of play-by-play data into team-level statistical summaries
- Regression model (`sklearn`) trained on team-level data of previous season

## Structure
```
root/
├── core/           # Key steps of pipeline
├── data/           # All files in data gitignored
│   ├── clean/      # Clean play-by-play data, intended for dataframe operations
│   ├── misc/       # All other data required by model
│   └── raw/        # Raw play-by-play data, directly pulled from NHL API
├── tests/          # Pytest suites
├── validation/     # Connection and structure checks
├── .gitignore
├── README.md
└── requirements.txt
```

## Rough Time Benchmarks
As my model continues to progess, I will make my best effort to track how fast my model runs its key steps.

### Ingestion
Due to rate-limiting on the NHL API, I tend to ingest all required data for the model in batches of 100 games with a time of no less than 1 hour between batch collections. Currently, I have obtained the following runtimes for each batch of 100 play-by-plays ingested:

- 2024 (1-100): 28.235 seconds
- 2024 (101-200): 28.158 seconds
- 2024 (201-300): 30.463 seconds

Based on the above runtimes, the model takes, on average, about 0.290 seconds to ingest one play-by-play directly from the NHL API.

### Cleaning/Compression
Cleaning the data is done post-ingestion, so, if done from raw data, the entire dataset can be cleaned in one pass.

As I have been cleaning my data directly after ingesting it raw from the API, my cleaning calls are also benchamrked in batches of 100. Currently, I have obtained the following runtimes for each batch of 100 play-by-plays cleaned:

- 2024 (1-100): 1.908 seconds
- 2024 (101-200): 2.129 seconds
- 2024 (201-300): 1.761 seconds

Based on the above runtimes, the model takes, on average, about 0.019 seconds to clean each play-by-play from the raw data.

### Breakdown of Overall Pipeline Time (So Far)
1. **Ingestion**
    
    As a season has 1312 total regular season games, we should expect one season to take about:
    
    $$1312gm*0.290s/gm \approx 380s$$

    6m 20s to fully ingest.
    
    Unfortunately, due to rate limiting on the NHL API, an entire season cannot be collected in one pass. As such, the actual time to get all data fully ingested is much longer.

2. **Cleaning/Compression**

    Doing the same calculation as we did above with ingestion, we find that, for an entire season of play-by-plays, the model takes:

    $$1312gm*0.019s/gm \approx 24.9s$$

    about 25 seconds to clean and compress the raw data into a more usable format.