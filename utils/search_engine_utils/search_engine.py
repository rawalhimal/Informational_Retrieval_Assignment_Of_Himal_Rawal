# my_crawler_package/search_engine.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from .inverted_index import InvertedIndex
from ..logging_config import setup_logger

import nltk
nltk.download('stopwords')
nltk.download('punkt')
import ast

class SearchEngine:
    def __init__(self, index_file='data/publications.csv'):
        """
        Initializes the SearchEngine with a TF-IDF vectorizer and CSV file.

        Parameters:
        index_file (str): The path to the CSV file containing the publication records.
        """
        self.index_file = index_file
        self.porter_stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.logger = setup_logger()

        # Load the inverted index
        self.inverted_index = InvertedIndex(file_path=self.index_file).generate_inverted_index()

        # Load and prepare the data
        self.dataframe = pd.read_csv(self.index_file)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.dataframe['Title of the Research Paper'])

    def preprocess_query(self, query):
        """
        Pre-processes the query string by tokenizing, stemming, and removing stop words.

        Parameters:
        query (str): The search query entered by the user.

        Returns:
        str: A processed query string.
        """
        tokens = word_tokenize(query.lower())
        stemmed_tokens = [self.porter_stemmer.stem(word) for word in tokens if word not in self.stop_words and word.isalpha()]
        return ' '.join(stemmed_tokens)

    def search(self, query):
        """
        Searches for the query in the TF-IDF matrix and returns ranked documents.

        Parameters:
        query (str): The search query entered by the user.

        Returns:
        list: A list of dictionaries containing publication details that match the query.
        """
        processed_query = self.preprocess_query(query)
        query_vector = self.vectorizer.transform([processed_query])
        cosine_similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        top_indices = cosine_similarities.argsort()[-10:][::-1]  # Get top 10 results

        results = []
        for index in top_indices:
            authors = self.dataframe.iloc[index]['Authors']
            profile_links = self.dataframe.iloc[index]['Pureportal Profile Link']
            
            # Assuming authors and profile_links are lists and need to be processed
            author_list = authors.strip("[]").replace("'", "").split(', ')
            profile_list = profile_links.strip("[]").replace("'", "").split(', ')

            results.append({
                'Title': self.dataframe.iloc[index]['Title of the Research Paper'],
                'Link': self.dataframe.iloc[index]['Link to the Research Paper'],
                'Published Date': self.dataframe.iloc[index]['Published Date'],
                'Authors': author_list,
                'Profile Links': profile_list
            })

        self.logger.info(f"Found {len(results)} results for the query.")
        return results
