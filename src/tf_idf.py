import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from owapy.tools.time_it import time_it
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity, euclidean_distances

from common_paths import join_to_local_dir

out_length = 10

# TODO: the main improvement here would be to have my own tokenizer. For example, insteaf of "slip and fall" being mapped to "slip" and "fall", it
#  should be mapped to "slip", "fall", and "slip and fall"

# TODO try everything on facebook posts data!!

# Sample data
data = {'ID1': 'This is a sample paragraph.',
        'ID2': 'Another example of text.',
        'ID3': 'Writing more examples.'}
df_path = join_to_local_dir("data", "Claim Adjusters Notes Sample (RRT-46784).xlsx")
df = pd.read_excel(df_path)

for index, row in df.iterrows():
    note = row['note']
    if isinstance(note, str):
        data[index] = note

# Pre-processing  # TODO add more steps? Removing from strings, map synonyms, etc
# TODO probably a good idea to break up sentences into different records. This way, smaller chance that all the words happen to all appear
#  randomly in a long document
df.dropna(subset='note', axis=0, inplace=True)
notes= df['note'].values

# Since this one uses normalized vectors (and cosine sim), a short note with just one of the key words could be given a high score.

# TODO it's worht noting that so far binary tf is probably best because my documents are very short. In general, sublinear-tf is used for large documents.
#  I don't think it would be good idea to group notes together (indeed I think we might want to do the opposite), but it could still be a good idea
#  to use sublinear-tf if it turns out we work with documents larger than ~ 10 words

def tfidf_with_reg_tf(query, notes):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(notes)
    # feature_names = tfidf_vectorizer.get_feature_names_out()
    query_vector = tfidf_vectorizer.transform([query])
    cosine_similarities = cosine_similarity(tfidf_matrix, query_vector.reshape(1, -1)).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-out_length:-1]
    print("Results for tf-idf with regular term frequency")
    print(notes[related_docs_indices])
    print("\n")


def tfidf_with_binary_tf(query, notes):
    # This one is closer to simply checking whether each word of the query is present in the note. In case of equality, unusual words will be given precedence
    # Tried different ways (normalzied, cosine) and this was the best
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', norm=None, binary=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(notes)
    query_vector = tfidf_vectorizer.transform([query])
    dot_products= tfidf_matrix.dot(query_vector.T).toarray().flatten()
    related_docs_indices = dot_products.argsort()[:-out_length:-1]
    print("Results for tf-idf with binary term frequency")
    print(notes[related_docs_indices])
    print("\n")


def tfidf_with_sublinear_tf(query, notes):
    # Tried sublinear term frequency in multiple ways, did not do very well
    # Tried different ways (unnormalzied, dot product) and this was the best
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', sublinear_tf=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(notes)
    # feature_names = tfidf_vectorizer.get_feature_names_out()
    query_vector = tfidf_vectorizer.transform([query])
    cosine_similarities = cosine_similarity(tfidf_matrix, query_vector.reshape(1, -1)).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-out_length:-1]
    print("Results for tf-idf with sublinear term frequency")
    print(notes[related_docs_indices])
    print("\n")


# TODO try Okapi BM25: This is a more complex variation that takes into account both term frequency and document length. It also uses a non-linear function to calculate the idf value.

# TODO it probably makes sense to do tf-idf first to at least filter notes that share any word with the prompt. Then we can use nlp on that subset
query = 'the employee is a customer accounts manager' # Binary tf is the best!
query = 'slip and fall'  # Binary tf is the best!
tfidf_with_reg_tf(query, notes)
tfidf_with_binary_tf(query, notes)
tfidf_with_sublinear_tf(query, notes)
