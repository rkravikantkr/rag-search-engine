import json

data_path = "../data/movies.json"


def get_movies_title(query) -> list:

    with open(data_path, "r") as f:
        # data is now a python dictionary
        data = json.load(f)
        movies = data["movies"]
        # print(f"title to look for: {query}")
        # print(f"total movies: {len(movies)}")

        title_list = []
        for movie in movies:
            title_list.append(movie["title"])

        for title in title_list:
            if title == query:
                print(f"found title: {title}")
    return title_list


mlist = get_movies_title("Now You Know")
print(mlist[:3])
