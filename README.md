# Informational_Retrieval_Assignment_Of_Himal_Rawal
The document clustering and search system is a tool that helps organize and retrieve information efficiently.

Summary:
This project incorporates a thorough system for organizing and searching documents. It is divided into two main components, which are located in the inside utils folder.

Search_engine_utils (ques1): 
encompasses modules for crawling, indexing, and searching publications.

Clustering_utils (ques2):
specializes in document clustering, data preprocessing, and evaluating clustering results.

Project Framework.

Data/: contains data extracted.
The model/vectorizer contains clustering capabilities.
Static: contains image for website.
Templated/:
Index.html/: website home page html script.
Results.html/:search engine result page script.
Clustering result page script.
Utils/:
Search_engine_utils/:
Web_crawler.py: contains the code for extracting data from coventry university publications, including the author, title, and name.
Scheduler.Py: manages the scheduling of periodic crawling, which is executed every Sunday at 10am.
Inverted_index.py: a Python module that implements an inverted index for searching publications.
Search_engine.Py: employs tf-idf vectorizer to conduct searches on articles.
Clustering_utils/clustering_utilspy:
Data_preprocessing.Py: manages the retrieval, preprocessing, and cleansing of textual data obtained from bbc rss feeds.
Document_clustering.Py: contains the necessary logic for clustering documents using various techniques.
The logging configuration logs each date's data in the logs folder.
Crawler_main.py: requires the search_engine_utils module to crawl the specified website.
Clustering_main.py: executes clustering using the module in the clustering_utils folder.
flask application.
The requirements.txt file specifies the necessary Python packages for the project.
Setup:
Install necessary packages.

Make sure you have the required python libraries installed. You can install them using the requirements.txt file.

pip install -r requirements.txt
Save profile,publications.

This module will save your profile and publications to a designated folder, allowing you to easily search for them in a search engine.

Python script_main.py.
Save clusturing model and vectorizer.

This module will save the most effective model and vectorizer which will be utilized during document clustering.

Python clustering_main.py.
Webpage:
To launch the website.
Python app_main.py
Logs:
These two folders are disregarded.

