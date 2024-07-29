import schedule
import time
from .web_crawler import WebCrawler
from ..logging_config import setup_logger

class CrawlerScheduler:
    def __init__(self, publications_url, profiles_url):
        """
        Initializes the CrawlerScheduler with the given URLs.

        Parameters:
        publications_url (str): The URL for the publications page.
        profiles_url (str): The URL for the profiles page.
        """
        self.publications_url = publications_url
        self.profiles_url = profiles_url
        self.logger = setup_logger()

    def job(self):
        """
        Scheduled job to initialize the WebCrawler and execute the crawling process.
        
        This method creates an instance of WebCrawler and invokes its run_crawler method. 
        Logs messages about the completion status of the crawling job.
        """
        self.logger.info("Starting the scheduled crawling job.")
        crawler = WebCrawler(self.publications_url, self.profiles_url)
        
        try:
            if crawler.run_crawler():
                self.logger.info("New data available and saved successfully.")
            else:
                self.logger.info("No new data available.")
        except Exception as e:
            self.logger.error(f"An error occurred during the crawling job: {e}")
        finally:
            self.logger.info("Scheduled crawling job completed.")

    def start_scheduler(self):
        """
        Starts the scheduler to run the crawling job once a week at a specified time.

        The scheduler will trigger the job function every week on Sunday at 10:00 AM. 
        It continuously checks and runs scheduled jobs while the program is active.
        """
        self.logger.info("Starting the scheduler.")
        schedule.every().sunday.at("10:00").do(self.job)
        self.logger.info("Scheduler started. Waiting for the scheduled job to run.")

        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_crawler_manual(self):
        """
        Runs the crawler manually and saves the data to a CSV file.
        """
        self.logger.info("Starting manual crawl.")
        self.job()
        self.logger.info("Manual crawl completed.")
