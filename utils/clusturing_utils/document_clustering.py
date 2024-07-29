# utils/ques2/document_clustering.py

import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib

class DocumentClustering:
    """
    DocumentClustering class for clustering documents using KMeans.

    Methods:
        fit(documents): Fits the model to the given documents.
        predict(new_documents): Predicts the clusters for new documents.
        get_silhouette_score(X, labels): Computes the silhouette score.
        get_cluster_details(): Retrieves details of each cluster.
        save(model_path, vectorizer_path): Saves the model and vectorizer to disk.
    """
    
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000, min_df=2, stop_words='english', use_idf=True)
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.logger = logging.getLogger(__name__)

    def fit(self, documents):
        """
        Fits the model to the given documents.

        Args:
            documents (list): List of preprocessed document texts.

        Returns:
            array: Transformed document vectors.
        """
        X = self.vectorizer.fit_transform(documents)
        self.model.fit(X)
        self.logger.info(f"Model fitted with {self.n_clusters} clusters.")
        return X

    def predict(self, new_documents):
        """
        Predicts the clusters for new documents.

        Args:
            new_documents (list): List of new document texts.

        Returns:
            array: Predicted cluster labels.
        """
        X_new = self.vectorizer.transform(new_documents)
        return self.model.predict(X_new)

    def get_silhouette_score(self, X, labels):
        """
        Computes the silhouette score for the given data and labels.

        Args:
            X (array): Transformed document vectors.
            labels (array): Cluster labels.

        Returns:
            float: Silhouette score.
        """
        score = silhouette_score(X, labels)
        self.logger.info(f"Silhouette Score: {score}")
        return score

    def get_cluster_details(self):
        """
        Retrieves details of each cluster, including the top terms.

        Returns:
            dict: Dictionary containing cluster details.
        """
        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names_out()
        cluster_details = {}
        for i in range(self.n_clusters):
            top_terms = [terms[ind] for ind in order_centroids[i, :10]]
            cluster_details[i] = {'terms': top_terms}
        return cluster_details

    def save(self, model_path, vectorizer_path):
        """
        Saves the model and vectorizer to disk.

        Args:
            model_path (str): Path to save the model.
            vectorizer_path (str): Path to save the vectorizer.
        """
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)
        self.logger.info(f"Model saved to {model_path} and vectorizer saved to {vectorizer_path}.")
    
    @classmethod
    def load(cls, model_path, vectorizer_path):
        """
        Loads the model and vectorizer.

        Args:
            model_path (str): Path to load the model.
            vectorizer_path (str): Path to load the vectorizer.

        Returns:
            DocumentClustering: Instance of DocumentClustering with loaded model and vectorizer.
        """
        instance = cls()
        instance.model = joblib.load(model_path)
        instance.vectorizer = joblib.load(vectorizer_path)
        return instance
