# main.py
from utils.clusturing_utils.data_preprocessing import DataPreprocessor
from utils.clusturing_utils.document_clustering import DocumentClustering
from utils.logging_config import setup_logger
import nltk

# Downloading necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
# Configure logger
logger = setup_logger()

def evaluate_model(documents, n_clusters):
    """
    Evaluates the KMeans clustering model using silhouette score.

    Args:
        documents (list): A list of preprocessed document texts.
        n_clusters (int): The number of clusters to evaluate.

    Returns:
        tuple: The silhouette score and the trained model.
    """
    logger.info(f"Evaluating model with {n_clusters} clusters...")
    clustering = DocumentClustering(n_clusters=n_clusters)
    X_transformed = clustering.fit(documents)
    labels = clustering.model.predict(X_transformed)
    score = clustering.get_silhouette_score(X_transformed, labels)
    
    # Log cluster details
    cluster_details = clustering.get_cluster_details()
    logger.info(f"Cluster details for {n_clusters} clusters:")
    for cluster_id, details in cluster_details.items():
        logger.info(f"Cluster {cluster_id}: Top Terms - {details['terms']}")
    
    return score, clustering

def main():
    """
    Main function to fetch documents, preprocess them, evaluate clustering methods,
    and save the best model.
    """
    logger.info("Starting model training and saving process.")

    # Define RSS feed URLs and categories
    categories = {
        'http://rss.cnn.com/rss/edition_sport.rss': 'Sports',
        'http://feeds.bbci.co.uk/news/technology/rss.xml': 'Technology',
        'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml': 'Entertainment',
        'http://feeds.bbci.co.uk/news/politics/rss.xml': 'Politics',
        'http://rss.cnn.com/rss/money_news_international.rss': 'Business'
    }

    # Initialize DataPreprocessor
    preprocessor = DataPreprocessor()
    
    # Fetch and preprocess documents
    logger.info("Fetching and preprocessing documents.")
    documents = preprocessor.fetch_and_preprocess(categories, list(categories.values()))
    preprocessor.create_word_cloud(documents)
    
    if not documents:
        logger.error("No documents available for clustering. Exiting.")
        return

    # Define the range of clusters to evaluate
    cluster_ranges = range(2, 6)  # Example range from 2 to 10 clusters
    best_score = -1
    best_model = None
    best_n_clusters = 0

    # Evaluate models with different cluster sizes
    for n_clusters in cluster_ranges:
        try:
            score, clustering = evaluate_model(documents, n_clusters)
            logger.info(f"Cluster count: {n_clusters}, Silhouette Score: {score}")
            if score > best_score:
                best_score = score
                best_model = clustering
                best_n_clusters = n_clusters
        except Exception as e:
            logger.error(f"Error evaluating model with {n_clusters} clusters: {e}")

    if best_model:
        # Save the best model and vectorizer
        best_model.save('./models/best_clustering_model.pkl', './models/best_vectorizer.pkl')
        logger.info(f"Best model with {best_n_clusters} clusters saved successfully.")
    else:
        logger.error("No suitable model found during evaluation.")

    logger.info("Model training and saving process completed.")

if __name__ == "__main__":
    main()

