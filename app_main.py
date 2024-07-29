from flask import Flask, render_template, request, redirect, url_for
from utils.search_engine_utils.search_engine import SearchEngine
from utils.clusturing_utils.document_clustering import DocumentClustering
from utils.clusturing_utils.data_preprocessing import DataPreprocessor
import joblib

app = Flask(__name__)

# Load the best clustering model and vectorizer
model_path = './models/best_clustering_model.pkl'
vectorizer_path = './models/best_vectorizer.pkl'

# Initialize DocumentClustering with error handling
try:
    clustering = DocumentClustering.load(model_path, vectorizer_path)
except Exception as e:
    app.logger.error(f"Error loading clustering model or vectorizer: {e}")
    clustering = None

# Initialize DataPreprocessor
preprocessor = DataPreprocessor()

# Initialize SearchEngine
search_engine = SearchEngine(index_file='data/publications.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form.get('query')
            if query:
                return redirect(url_for('results', query=query))
        elif 'document' in request.form:
            document = request.form.get('document')
            if document:
                return redirect(url_for('classify_result', document=document))
    return render_template('index.html')

@app.route('/results')
def results():
    query = request.args.get('query')
    results = []
    if query:
        results = search_engine.search(query)
        for result in results:
            authors = result.get('Authors', [])
            profile_links = result.get('Profile Links', [])
            if len(authors) != len(profile_links):
                profile_links = profile_links[:len(authors)]
            result['AuthorProfilePairs'] = list(zip(authors, profile_links))
    return render_template('results.html', results=results)

@app.route('/cluster_result')
def classify_result():
    document = request.args.get('document')
    cluster = None
    cluster_info = None
    if document and clustering:
        try:
            # Preprocess the document
            preprocessed_doc = preprocessor._preprocess_text(document)
            print(preprocessed_doc)
            
            # Transform the preprocessed document into a vector
            doc_vector = clustering.vectorizer.transform([preprocessed_doc])
            print(doc_vector)
            
            # Predict the cluster
            cluster = clustering.model.predict(doc_vector)[0]


            # Retrieve cluster details
            cluster_details = clustering.get_cluster_details()
            cluster_info = cluster_details.get(cluster, {})
        except ValueError as e:
            print(f"Error retrieving cluster details: {e}")
        except Exception as e:
            print(f"Error in document classification: {e}")

    return render_template('cluster_result.html', document=document, cluster=cluster, cluster_info=cluster_info)

if __name__ == "__main__":
    app.run(debug=True)



