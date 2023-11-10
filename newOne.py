# import os
# import pymongo
# import re
# import math
# from bs4 import BeautifulSoup
# from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer
#
# # Initialize SnowballStemmer for English
# stemmer = SnowballStemmer("english")
#
# # Define MongoDB connection
# mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
# mongo_db = mongo_client["Web_Indexing"]
# mongo_collection = mongo_db["Words and Links"]
# # Define a new collection for document number to link mapping
# document_link_collection = mongo_db["DocumentLinkCollection"]
#
# # Definition tag priorities
# tag_priorities = {
#     'title': 1,
#     'h1': 2,
#     'h2': 3,
#     'h3': 4,
#     'h4': 5,
#     'h5': 6,
#     'h6': 7,
#     'p': 8,
#     'div': 9,
#     'span': 10,
# }
#
# # Function to preprocess text-
# def preprocess_text(text):
#     # Tokenize, remove punctuation, lowercase, apply stemming, and remove stopwords
#     tokens = re.findall(r'\b\w+\b', text.lower())
#     tokens = [stemmer.stem(token) for token in tokens if token not in stopwords.words('english')]
#     return tokens
#
# # Function to calculate TF-IDF for a term in a document
# def calculate_tf_idf(term, doc_tokens, doc_count, inverted_index):
#     tf = doc_tokens.count(term) / len(doc_tokens)
#     idf = math.log(doc_count / (len(inverted_index.get(term, [])) + 1))
#     return tf * idf
#
# # Function to process an HTML document
# def process_html_document(html_content, document_count, website_link):
#
#     # Parsing HTML
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#     # Create a dictionary to store keyword frequencies
#     keyword_frequencies = {}
#
#     for tag, priority in tag_priorities.items():
#         elements = soup.find_all(tag)
#         for element in elements:
#             text = element.get_text(strip=True)
#             if text:
#                 # Preprocess and stem the text
#                 tokens = preprocess_text(text)
#                 for token in tokens:
#                     if token not in keyword_frequencies:
#                         keyword_frequencies[token] = {
#                             'documents': [{
#                                 'no': document_count,
#                                 'freq': tokens.count(token),
#                                 'priority': tag_priorities[tag],
#                                 'tf-idf': 0.0,
#                                 'link': website_link,
#                             }],
#                         }
#                     else:
#                         existing_entry = keyword_frequencies[token]['documents'][0]
#                         if tag_priorities[tag] < existing_entry['priority']:
#                             existing_entry['priority'] = tag_priorities[tag]
#                         existing_entry['freq'] += tokens.count(token)
#
#     # Store the HTML text content in the 'html' field of the document
#     return {
#         'document_number': document_count,
#         'keyword_frequencies': keyword_frequencies,
#     }
#
# # Main loop to process HTML documents and calculate TF-IDF
# document_count = 1
# documents = []
#
# base_directory = 'C:\\Users\\HP\\crawler-bucket\\Folder_1'
# print(f"Base Directory: {base_directory}")
#
# for website_link in os.listdir(base_directory):
#     website_folder = os.path.join(base_directory, website_link)
#     if os.path.isdir(website_folder):
#         try:
#             # Check for HTML files and process them
#             html_files = [f for f in os.listdir(website_folder) if f.endswith(('.html', '.htm'))]
#             if html_files:
#                 html_path = os.path.join(website_folder, html_files[0])  # Use the first HTML file found
#                 with open(html_path, 'r', encoding='utf-8', errors='ignore') as html_file:
#                     html_content = html_file.read()
#                 document_data = process_html_document(html_content, document_count, website_link)
#                 if document_data:
#                     documents.append(document_data)
#                     document_count += 1
#                     print(f"Document {document_count - 1} indexed for website: {website_link}")
#             else:
#                 print(f"No HTML file found for website: {website_link}")
#         except Exception as e:
#             print(f"Error processing website {website_link}: {str(e)}")
#
# # Word-wise index
# word_wise_index = {}
#
# for doc in documents:
#     for term, frequencies in doc['keyword_frequencies'].items():
#         if term not in word_wise_index:
#             word_wise_index[term] = []
#
#         for entry in frequencies['documents']:
#             word_info = {
#                 'doc_no': entry['no'],
#                 'frequency': entry['freq'],
#                 'priority': entry['priority'],
#                 'tf-idf': calculate_tf_idf(term, [t for t in doc['keyword_frequencies']], len(documents), word_wise_index),
#                 'link': entry['link'],
#             }
#             word_wise_index[term].append(word_info)
#
# # Store word-wise index in MongoDB
# for word, info_list in word_wise_index.items():
#     mongo_collection.insert_one({
#         'word': word,
#         'info_list': info_list,
#     })
#
# # Create a list of document number and corresponding link
# document_links = [
#     {
#         'document_number': doc['document_number'],
#         'link': website_link  # Use the website link as the 'link' field
#     }
#     for doc, website_link in zip(documents, os.listdir(base_directory))
# ]
#
# # Sort the list by document number in ascending order
# document_links.sort(key=lambda x: x['document_number'])
#
# # Insert the sorted document number to link mapping into the collection
# for link_mapping in document_links:
#     document_link_collection.insert_one(link_mapping)
#
#
# mongo_client.close()
import os
import pymongo
import re
import math
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Initialize SnowballStemmer for English
stemmer = SnowballStemmer("english")

# Define MongoDB connection
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["Web_Indexing_freq"]
mongo_collection = mongo_db["Words and Links"]
# Define a new collection for document number to link mapping
document_link_collection = mongo_db["DocumentLinkCollection"]

# Definition tag priorities
tag_priorities = {
    'title': 1,
    'h1': 2,
    'h2': 3,
    'h3': 4,
    'h4': 5,
    'h5': 6,
    'h6': 7,
    'p': 8,
    'div': 9,
    'span': 10,
}

# Function to preprocess text-
def preprocess_text(text):
    # Tokenize, remove punctuation, lowercase, apply stemming, and remove stopwords
    tokens = re.findall(r'\b\w+\b', text)  # Removed lowercasing here
    tokens = [stemmer.stem(token) for token in tokens if token not in stopwords.words('english')]
    return tokens

# Function to calculate TF-IDF for a term in a document
def calculate_tf_idf(term, doc_tokens, doc_count, inverted_index):
    tf = doc_tokens.count(term) / len(doc_tokens)
    idf = math.log(doc_count / (len(inverted_index.get(term, [])) + 1))
    return tf * idf

# Function to process an HTML document
def process_html_document(html_content, document_count, website_link):

    # Parsing HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a dictionary to store keyword frequencies
    keyword_frequencies = {}

    for tag, priority in tag_priorities.items():
        elements = soup.find_all(tag)
        for element in elements:
            text = element.get_text(strip=True)
            if text:
                # Preprocess and stem the text
                tokens = preprocess_text(text)
                for token in tokens:
                    if token not in keyword_frequencies:
                        keyword_frequencies[token] = {
                            'documents': [{
                                'no': document_count,
                                'freq': tokens.count(token),
                                'priority': tag_priorities[tag],
                                'tf-idf': 0.0,
                                'link': website_link,
                            }],
                        }
                    else:
                        existing_entry = keyword_frequencies[token]['documents'][0]
                        if tag_priorities[tag] < existing_entry['priority']:
                            existing_entry['priority'] = tag_priorities[tag]
                        existing_entry['freq'] += tokens.count(token)

    # Store the HTML text content in the 'html' field of the document
    return {
        'document_number': document_count,
        'keyword_frequencies': keyword_frequencies,
    }

# Main loop to process HTML documents and calculate TF-IDF
document_count = 1
documents = []

base_directory = 'C:\\Users\\HP\\crawler-bucket\\Folder_1'
print(f"Base Directory: {base_directory}")

for website_link in os.listdir(base_directory):
    website_folder = os.path.join(base_directory, website_link)
    if os.path.isdir(website_folder):
        try:
            # Check for HTML files and process them
            html_files = [f for f in os.listdir(website_folder) if f.endswith(('.html', '.htm'))]
            if html_files:
                html_path = os.path.join(website_folder, html_files[0])  # Use the first HTML file found
                with open(html_path, 'r', encoding='utf-8', errors='ignore') as html_file:
                    html_content = html_file.read()
                document_data = process_html_document(html_content, document_count, website_link)
                if document_data:
                    documents.append(document_data)
                    document_count += 1
                    print(f"Document {document_count - 1} indexed for website: {website_link}")
            else:
                print(f"No HTML file found for website: {website_link}")
        except Exception as e:
            print(f"Error processing website {website_link}: {str(e)}")

# Word-wise index
word_wise_index = {}

for doc in documents:
    for term, frequencies in doc['keyword_frequencies'].items():
        if term not in word_wise_index:
            word_wise_index[term] = []

        for entry in frequencies['documents']:
            word_info = {
                'doc_no': entry['no'],
                'frequency': entry['freq'],
                'priority': entry['priority'],
                'tf-idf': calculate_tf_idf(term, [t for t in doc['keyword_frequencies']], len(documents), word_wise_index),
                'link': entry['link'],
            }
            word_wise_index[term].append(word_info)

# Store word-wise index in MongoDB
for word, info_list in word_wise_index.items():
    mongo_collection.insert_one({
        'word': word,
        'info_list': info_list,
    })

# Create a list of document number and corresponding link
document_links = [
    {
        'document_number': doc['document_number'],
        'link': website_link  # Use the website link as the 'link' field
    }
    for doc, website_link in zip(documents, os.listdir(base_directory))
]


# Sort the list by document number in ascending order
document_links.sort(key=lambda x: x['document_number'])

# Insert the sorted document number to link mapping into the collection
for link_mapping in document_links:
    document_link_collection.insert_one(link_mapping)
# import pymongo

# Initialize a connection to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Web_Indexing_freq"]  # Use your database name

# Define the search term
search_term = input("Enter your Query: ")

# Find documents that contain the search term
results = db["Words and Links"].find({
    "word": search_term
})

# Print all matching documents
for result in results:
    for entry in result['info_list']:
        print(f"Document Number: {entry['doc_no']}")
        print(f"Link: {entry['link']}")
        print(f"TF-IDF: {entry['tf-idf']}")
        print("\n")

# Close the MongoDB connection
client.close()

mongo_client.close()
