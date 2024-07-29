# my_crawler_package/web_crawler.py
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
from urllib.error import HTTPError

from ..logging_config import setup_logger

class WebCrawler:
    def __init__(self, publications_url, profiles_url):
        """
        Initializes the WebCrawler with the given URLs.

        Parameters:
        publications_url (str): The URL for the publications page.
        profiles_url (str): The URL for the profiles page.
        """
        self.publications_url = publications_url
        self.profiles_url = profiles_url
        self.logger = setup_logger()

    def check_allowed_robots(self) -> bool:
        """
        Checks whether the given URL is allowed to be crawled based on the robots.txt rules.

        Parameters:
        url (str): The URL to check.

        Returns:
        bool: True if the URL can be crawled, False otherwise.
        """
        url = 'https://pureportal.coventry.ac.uk'
        self.logger.info(f"Checking robots.txt for URL: {url}")
        robot_parser = RobotFileParser()
        robot_parser.set_url(urljoin(url, "/robots.txt"))
        try:
            robot_parser.read()
            self.logger.info("Robots.txt read successfully.")
            return robot_parser.can_fetch("*", url)
        except HTTPError:
            self.logger.error("Failed to read robots.txt.")
            return False

    def fetch_profiles(self) -> list:
        """
        Fetches and returns a list of profile links from the profiles URL.

        Returns:
        list: A list of profile links.
        """
        self.logger.info("Fetching profile details.")
        self.check_allowed_robots()
        profile_links = []
        profiles = requests.get(self.profiles_url)
        self.logger.info(self.profiles_url)
        profiles_soup = BeautifulSoup(profiles.content, 'html.parser')
        profiles_lists = profiles_soup.find_all('div', class_="result-container")

        for lists in profiles_lists:
            for profile in lists.find_all("a", class_="link person"):
                profile_links.append(profile.get('href'))
        self.logger.info("Profile details retrieved.")

        return profile_links

    def fetch_publications(self) -> list:
        """
        Fetches publication details from the publications URL.

        Returns:
        list: A list of dictionaries containing publication details.
        """
        self.logger.info("Fetching publication details.")
        publication_results = []
        while True:
            publications = requests.get(self.publications_url)
            publications_soup = BeautifulSoup(publications.content, 'html.parser')
            publications_lists = publications_soup.find_all('div', class_="result-container")

            for paper in publications_lists:
                publication = self.extract_publication_details(paper)
                if publication:
                    publication_results.append(publication)

            next_link = publications_soup.find("a", class_="nextLink")
            if not next_link:
                break
            self.logger.info("Moving to the next page of publications.")
            self.publications_url = 'https://pureportal.coventry.ac.uk' + next_link["href"]

        self.logger.info("All publication details fetched.")
        return publication_results

    def extract_publication_details(self, paper) -> dict:
        """
        Extracts details of a single publication.

        Parameters:
        paper (BeautifulSoup object): The BeautifulSoup object representing the publication.

        Returns:
        dict: A dictionary containing publication details, or None if no valid data found.
        """
        author_names = []
        author_profile_links = []
        dictionary = {}

        title = paper.find("h3", class_="title")
        paper_link = paper.find("a", class_="link")
        published_date = paper.find("span", class_="date")

        if title and paper_link and published_date:
            for author in paper.find_all("a", class_="link person"):
                author_names.append(author.string)
                author_profile_links.append(author.get('href'))

            dictionary['Title of the Research Paper'] = title.text
            dictionary['Link to the Research Paper'] = paper_link.get('href')
            dictionary['Published Date'] = published_date.text
            dictionary['Authors'] = author_names
            dictionary['Pureportal Profile Link'] = author_profile_links

            return dictionary
        return None

    def save_profiles_to_csv(self, profiles):
        """
        Saves the fetched profile links to a CSV file in the 'data' folder.

        Parameters:
        profiles (list): A list of profile links.
        """
        if profiles:
            self.logger.info("Saving profile links to CSV file.")
            df = pd.DataFrame(profiles, columns=['Profile Links'])
            os.makedirs('data', exist_ok=True)
            df.to_csv('data/profiles.csv', index=False, encoding="utf-8")
            self.logger.info("Profile links saved successfully to 'data/profiles.csv'.")

    def save_publications_to_csv(self, publications):
        """
        Saves the fetched publication results to a CSV file in the 'data' folder.

        Parameters:
        publications (list): A list of dictionaries containing publication details.
        """
        if publications:
            self.logger.info("Saving publication details to CSV file.")
            df = pd.DataFrame(publications)
            os.makedirs('data', exist_ok=True)
            df.to_csv('data/publications.csv', index=False, encoding="utf-8")
            self.logger.info("Publication details saved successfully to 'data/publications.csv'.")

    def run_crawler(self) -> bool:
        """
        Runs the web crawler to fetch and save data from the publications and profiles URLs.

        Returns:
        bool: True if new data was found and saved, False otherwise.
        """
        self.logger.info("Starting web crawling process.")
        profile_links = self.fetch_profiles()
        publication_results = self.fetch_publications()

        new_data_found = False
        if publication_results:
            new_data_found = True
            self.save_publications_to_csv(publication_results)

        if profile_links:
            new_data_found = True
            self.save_profiles_to_csv(profile_links)

        self.logger.info("Web crawling process completed.")
        return new_data_found
