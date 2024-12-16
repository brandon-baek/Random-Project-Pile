def movie_rating_score():
    movie_ratings = {}
    movie_rating_data = open('movie_ratings.txt').read().split('\nSPLIT\n\n')
    for movie in movie_rating_data:
        movie_data = movie.split('\n')
        movie_ratings[movie_data[0]] = []
        for rating in movie_data[1:]:
            rating_details = rating.split(' -')
            if len(rating_details) > 1 and rating_details[1]:
                movie_ratings[movie_data[0]].append((rating_details[0], int(rating_details[1])))
    return movie_ratings

movie_ratings = movie_rating_score()