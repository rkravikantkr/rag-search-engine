#!/usr/bin/env python3

import argparse
import json
import string
from pathlib import Path

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

data_file_path = Path(__file__).parents[1].joinpath("data", "movies.json")
stopwords_file_path = Path(__file__).parents[1].joinpath("data", "stopwords.txt")


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
    return text.split()


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


def keyword_search(query) -> list:

    titles = load_movies_data()

    """ search for title containing search query """
    results = [
        title
        for title in titles
        if match_token(
            remove_punctuation(query).lower(), remove_punctuation(title).lower()
        )
    ]
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}\n")
            for *_, title in enumerate(keyword_search(args.query)):
                print(f"{title}")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
