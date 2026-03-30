#!/usr/bin/env python3

import argparse
import math
import sys

from utils.lib import InvertedIndex, keyword_search, tokenize

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

    idf_parser = subparsers.add_parser("idf", help="inverse document frequency")
    idf_parser.add_argument("term", type=str, help="require a term")

    tfidf_parser = subparsers.add_parser(
        "tfidf", help="term frequency-inverse document frequency"
    )
    tfidf_parser.add_argument("doc_id", type=int, help="require a document id")
    tfidf_parser.add_argument("term", type=str, help="require a term")

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
            inverted_index.build()
            inverted_index.save()

        case "tf":
            inverted_index.load()
            # 0 is printed when term doesn't exist,
            print(inverted_index.get_tf(args.doc_id, args.term))

        case "idf":
            # load index and docmap
            inverted_index.load()
            # calculate idf_value for given term
            term = args.term
            # print(tokenize(term))
            # print(len(inverted_index.index[tokenize(term)[0]]))

            idf_value = math.log(
                (len(inverted_index.docmap) + 1)
                / (len(inverted_index.index[tokenize(args.term)[0]]) + 1)
            )
            print(f"Inverse document frequency of '{args.term}': {idf_value:.2f}")

        case "tfidf":
            inverted_index.load()
            tf = inverted_index.get_tf(args.doc_id, args.term)
            idf = math.log(
                (len(inverted_index.docmap) + 1)
                / (len(inverted_index.index[tokenize(args.term)[0]]) + 1)
            )

            tf_idf = tf * idf

            print(
                f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tf_idf:.2f}"
            )

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
