import tmdbsimple as tmdb

tmdb.API_KEY = '454b6ca4172e455fe7a7d8395c10d6d9'
search = tmdb.Search()
movies = tmdb.Movies()


def get_movie_data(title):
    search.movie(query=title)
    return search.results


def get_popular_movies():
    top_rated = movies.top_rated()["results"]
    popular = movies.popular()["results"]
    upcoming = movies.upcoming()["results"]

    return top_rated + popular + upcoming


if __name__ == '__main__':
    movie_list = get_popular_movies()
    print(movie_list[0])