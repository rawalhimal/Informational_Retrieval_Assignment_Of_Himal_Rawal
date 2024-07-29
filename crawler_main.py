from utils.search_engine_utils.scheduler import CrawlerScheduler
from utils.logging_config import setup_logger

def main():
    """
    Main entry point for the script, allowing the user to choose between manual run or scheduled run.
    """
    # Set up the logger
    logger = setup_logger()
    logger.info("Crawl Program started.")
    
    
    try:
        user_input = input(
        """
        Below are your options to run the crawler. 
        a. Run the crawler manually (This will crawl the data now and create a CSV file). 
        b. Start the scheduler (This will run every Sunday and will update the CSV file with new entries. No manual input needed). 
        Make your choice (a or b) and provide the same as input.: 
        """
        ).lower()
        
        main_url = 'https://pureportal.coventry.ac.uk/en/organisations/eec-school-of-computing-mathematics-and-data-sciences-cmds/'
        publications_url = f'{main_url}/publications/'
        profiles_url =  f'{main_url}/persons/'

        scheduler = CrawlerScheduler(publications_url, profiles_url)
        
        if user_input == 'a':
            logger.info("User selected to run the crawler manually.")
            scheduler.run_crawler_manual()
        elif user_input == 'b':
            logger.info("User selected to schedule the crawler run.")
            scheduler.start_scheduler()
        else:
            logger.error("Invalid input provided. Please choose either (a) or (b).")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    logger.info("Crawl Program ended. \n\n")

if __name__ == "__main__":
    main()
