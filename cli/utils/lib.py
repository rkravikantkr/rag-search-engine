import json
import os
import pickle
import string
from collections import defaultdict
from pathlib import Path

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

data_file_path = Path(__file__).parents[2].joinpath("data", "movies.json")
stopwords_file_path = Path(__file__).parents[2].joinpath("data", "stopwords.txt")


class InvertedIndex:
    def __init__(self):
        """index attribute: a dictionary mapping tokens(strings) to sets of docs IDs(integers)"""
        self.index = defaultdict(set)

        """docmap attribute: a mapping document IDs to their full document object(each movie is a dict)"""
        self.docmap = {}

    # method to populate index
    def __add_document(self, doc_id, text):
        """Tokenize the input text, then add each token to the index with the doc ID"""
        tokens = tokenize(text)
        for token in tokens:
            self.index[token].add(doc_id)

    def get_documents(self, term) -> list:  # return a list of doc ids
        """Get the doc IDs for a given token and return as a list, sorted in ascending order"""
        return sorted(self.index[term.lower()])

    def build(self):
        """Iterate over all the movies and add them to both index and docmap"""
        with open(data_file_path, "r") as f:
            data = json.load(f)
        movies = data["movies"]

        doc_ids = [m["id"] for m in movies]
        self.docmap = dict(zip(doc_ids, movies))

        for m in movies:
            self.__add_document(doc_id=m["id"], text=f"{m['title']} {m['description']}")

    def save(self):
        os.makedirs("./cache", exist_ok=True)
        with open("./cache/index.pkl", "wb") as f:  # "wb" write binary
            pickle.dump(self.index, f)
        with open("./cache/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)

    def load(self):
        if not os.path.exists("./cache/index.pkl") or not os.path.exists(
            "./cache/docmap.pkl"
        ):
            raise FileNotFoundError("Cache not found. Run 'build' command first.")

        with open("./cache/index.pkl", "rb") as f:  # "rb" read binary
            self.index = pickle.load(f)
        with open("./cache/docmap.pkl", "rb") as f:
            self.docmap = pickle.load(f)


def load_stopwords() -> list:
    """Read stopwords file"""
    with open(stopwords_file_path, "r") as f:
        return f.read().splitlines()


def load_movies_data() -> list:
    """Load movies data into dictionary"""
    with open(data_file_path, "r") as f:
        data = json.load(f)

        """Iterating over movies list under key movies"""
        movies = data["movies"]
        titles = [movie["title"] for movie in movies]

    """Return list of titles in movie dataset"""
    return titles


def tokenize(text) -> list:
    text = remove_punctuation(text.lower())  # 1. clean
    tokens = text.split()  # 2. split into words
    return [stemmer.stem(token) for token in tokens]  # 3. stem each token


def remove_punctuation(text) -> str:
    """Removes all standard ASCII punctuation from a string."""
    # Create a translation table where all punctuation characters are mapped to None
    translator = str.maketrans("", "", string.punctuation)
    # Use the translate method to apply the mapping
    return text.translate(translator)


def filter_text(text: list) -> list:
    stopwords = load_stopwords()
    """Remove any stopwords from the user query tokens and title tokens before matching"""
    filtered_text = [t for t in text if t not in stopwords]
    return filtered_text


def match_token(query, title) -> bool:
    """Allow matches where at least one token from query matches any part of token from title."""

    """Tokenized query and title string"""
    query = tokenize(remove_punctuation(query).lower())
    title = tokenize(remove_punctuation(title).lower())

    """Filter query and title tokens"""
    query = filter_text(query)
    title = filter_text(title)

    """Reduce each token to its root(stemmed form)"""
    query = [stemmer.stem(token) for token in query]
    title = [stemmer.stem(token) for token in title]

    """partial or full matching query tokens"""
    query_tokens = [q for q in query for t in title if q in t]

    return len(query_tokens) != 0


def keyword_search(query, inverted_index) -> list:
    results = []
    tokens = tokenize(query)

    for token in tokens:
        # 1. get doc IDs for this token
        doc_ids = inverted_index.get_documents(token)

        # 2. for each doc ID, get the full document from docmap
        for id in doc_ids:
            results.append(inverted_index.docmap[id])
            if len(results) >= 5:
                return results
