# my_crawler_package/inverted_index.py

import os
import re
import pandas as pd
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from ..logging_config import setup_logger

class InvertedIndex:
    def __init__(self, file_path='data/publications.csv'):
        """
        Initializes the InvertedIndex class with the path to the CSV file.

        Parameters:
        file_path (str): Path to the CSV file containing publication titles.
        """
        self.file_path = file_path
        self.logger = setup_logger()
        self.inverted_index = {}

    def load_data(self) -> pd.DataFrame:
        """
        Loads data from the specified CSV file.

        Returns:
        pd.DataFrame: DataFrame containing publication details.
        """
        if not os.path.isfile(self.file_path):
            self.logger.error("The specified file is missing. Ensure the crawler has generated it.")
            return None

        self.logger.info(f"Loading data from {self.file_path}.")
        df = pd.read_csv(self.file_path)
        self.logger.info(f"Loaded data with {len(df)} entries.")
        return df

    def preprocess_titles(self, titles: pd.Series) -> list:
        """
        Pre-processes the titles by removing unwanted characters and stopwords.

        Parameters:
        titles (pd.Series): Series of titles to process.

        Returns:
        list: A list of processed titles.
        """
        stemmer = PorterStemmer()
        stop_words = set(stopwords.words('english'))
        processed_titles = []

        for title in titles:
            title = re.sub(r'[^\x00-\x7F]', '', title)
            title = re.sub(r'@\w+', '', title)
            title = title.lower()
            title = re.sub(r'[^\w\s]', '', title)
            title = ' '.join(word for word in title.split() if word not in stop_words)
            processed_titles.append(title)
        
        return processed_titles

    def tokenize_and_stem(self, titles: list) -> list:
        """
        Tokenizes and stems the titles.

        Parameters:
        titles (list): List of processed titles.

        Returns:
        list: List of tokenized and stemmed titles.
        """
        stemmer = PorterStemmer()
        tokenized_and_stemmed_titles = []

        for title in titles:
            tokens = word_tokenize(title)
            stemmed_tokens = [stemmer.stem(token) for token in tokens if token.isalpha()]
            tokenized_and_stemmed_titles.append(' '.join(stemmed_tokens))
        
        return tokenized_and_stemmed_titles

    def create_index(self, titles: list) -> dict:
        """
        Creates the inverted index from the tokenized and stemmed titles.

        Parameters:
        titles (list): List of tokenized and stemmed titles.

        Returns:
        dict: The inverted index mapping tokens to document indices.
        """
        inverted_index = {}

        for idx, title in enumerate(titles):
            tokens = title.split()
            for token in tokens:
                if token in inverted_index:
                    inverted_index[token].append(idx)
                else:
                    inverted_index[token] = [idx]
        
        return inverted_index

    def generate_inverted_index(self):
        """
        Generates the inverted index and logs the process.
        
        Returns:
        dict: The generated inverted index.
        """
        self.logger.info("Starting the creation of the inverted index.")
        df = self.load_data()

        if df is not None:
            titles = df['Title of the Research Paper'].astype(str)
            processed_titles = self.preprocess_titles(titles)
            tokenized_and_stemmed_titles = self.tokenize_and_stem(processed_titles)
            self.inverted_index = self.create_index(tokenized_and_stemmed_titles)
            self.logger.info("Inverted index creation completed.")
            return self.inverted_index
        else:
            self.logger.error("Failed to create the inverted index due to missing data.")
            return None
