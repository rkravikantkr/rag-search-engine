#!/usr/bin/env python3

import argparse
import json
import string
from pathlib import Path

data_path = Path(__file__).parents[1].joinpath("data", "movies.json")


def remove_punctuation(text) -> str:
    """Removes all standard ASCII punctuation from a string."""
    # Create a translation table where all punctuation characters are mapped to None
    translator = str.maketrans("", "", string.punctuation)
    # Use the translate method to apply the mapping
    return text.translate(translator)


def keyword_search(query) -> list:
    """load movie data into dictionary"""
    with open(data_path, "r") as f:
        data = json.load(f)

    """ iterating over movies list under key movies """
    movies = data["movies"]
    titles = [movie["title"] for movie in movies]

    """ cleaned punctuation query """
    query = remove_punctuation(query)

    """ search for title containing search query """
    results = [
        title for title in titles if query.lower() in remove_punctuation(title).lower()
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
