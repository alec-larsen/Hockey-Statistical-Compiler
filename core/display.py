def get_menu_option():
    return input("Please choose one of the following functionalities to execute:\n"
      + "1. Ingestion pass: Ingest 100 play-by-plays from the NHL API\n"
      + "2. Cleaning pass: Clean all previously ingested raw data.\n"
      + "3. Exit.\n")
