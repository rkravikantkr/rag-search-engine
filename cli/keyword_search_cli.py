#!/usr/bin/env python3

import argparse
import sys

from utils.lib import InvertedIndex, keyword_search

# instance / object of InvertedIndex class
inverted_index = InvertedIndex()


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build inverted index")

    tf_parser = subparsers.add_parser("tf", help="term frequency")
    tf_parser.add_argument("doc_id", type=int, help="require document id")
    tf_parser.add_argument("term", type=str, help="require a term")

    args = parser.parse_args()

    match args.command:
        case "search":
            try:
                # load the index
                inverted_index.load()
            except FileNotFoundError:
                print("Error: Cache not found. Run 'build' command first.")
                sys.exit(1)  # stop the program

            print(f"Searching for: {args.query}\n")

            for doc in keyword_search(args.query, inverted_index):
                print(f"{doc['title']} {doc['id']}")

        case "build":
            print("building inverted index")
            inverted_index.build()
            inverted_index.save()
            print("build successful!")

        case "tf":
            inverted_index.load()
            # 0 is printed when term doesn't exist,
            print(inverted_index.get_tf(args.doc_id, args.term))

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
