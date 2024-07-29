# utils/ques2/data_preprocessing.py

import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer
import feedparser
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import wordnet as wn

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

class DataPreprocessor:
    """
    DataPreprocessor class for fetching and preprocessing text data from RSS feeds.

    Methods:
        fetch_and_preprocess(categories, labels): Fetches and preprocesses text data from given RSS feed URLs.
    """
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.logger = logging.getLogger(__name__)

    def _preprocess_text(self, text):
        """
        Preprocess a given text by tokenizing, removing stopwords, and lemmatizing.

        Args:
            text (str): Text to preprocess.

        Returns:
            str: Preprocessed text.
        """
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        lemmatized_tokens = [self.lemmatizer.lemmatize(token.lower(), self._get_wordnet_pos(pos)) 
                             for token, pos in pos_tags if token.isalpha() 
                             and token.lower() not in self.stop_words]
        return ' '.join(lemmatized_tokens)

    def fetch_and_preprocess(self, categories, labels):
        """
        Fetches and preprocesses text data from given RSS feed URLs.

        Args:
            categories (dict): Dictionary of RSS feed URLs and their corresponding categories.
            labels (list): List of category labels.

        Returns:
            list: List of preprocessed documents.
        """
        documents = []
        for url, label in categories.items():
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                preprocessed_text = self._preprocess_text(title + ' ' + summary)
                documents.append(preprocessed_text)

                self.logger.info(f"Processed document from category {label}.")
        return documents
    
    def create_word_cloud(self, documents):
        """
        Create and display a word cloud from the preprocessed documents.

        Args:
            documents (list): List of preprocessed documents.
        """
        text = ' '.join(documents)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
    
    def _get_wordnet_pos(self, treebank_tag):
        """
        Convert treebank POS tag to WordNet POS tag.

        Args:
            treebank_tag (str): Treebank POS tag.

        Returns:
            str: WordNet POS tag.
        """
        if treebank_tag.startswith('J'):
            return wn.ADJ
        elif treebank_tag.startswith('V'):
            return wn.VERB
        elif treebank_tag.startswith('N'):
            return wn.NOUN
        elif treebank_tag.startswith('R'):
            return wn.ADV
        else:
            return wn.NOUN