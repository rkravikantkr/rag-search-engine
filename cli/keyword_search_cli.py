#!/usr/bin/env python3

import argparse

from utils.lib import InvertedIndex, keyword_search

# instance / object of InvertedIndex class
inverted_index = InvertedIndex()


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build inverted index")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}\n")
            for *_, title in enumerate(keyword_search(args.query)):
                print(f"{title}")

        case "build":
            print("building inverted index")
            inverted_index.build()
            inverted_index.save()
            print(
                f"First document for 'merida': {inverted_index.get_documents('merida')[0]}"
            )

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
