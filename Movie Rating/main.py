from difflib import get_close_matches as gcm
from numpy import average as weighted_avg
from os import system as sys

from movie_rating_data import movie_ratings


people = [
    'Lina', 'Nathan', 'Brian', 'Brandon', 'Brynn'
]

user_input = input('Name? (Or enter "all" to view all names)\n')
while user_input.lower() == 'all':
    sys('clear')
    for i in people:
        print(i)
    user_input = input('Name? (Or enter "all" to view all names)\n')

user_name = gcm(user_input,
                people,
                1,
                0)[0]

sys('clear')

print(f'Welcome {user_name},\n')

not_watched = []
for movie in movie_ratings:
    names = []
    for rating in movie_ratings[movie]:
        names.append(rating[0])
    if user_name.lower() not in names:
        not_watched.append(movie)

weights = {
    'lina': 10,
    'nathan': 10,
    'brian': 10,
    'brandon': 10,
    'brynn': 10
}
del weights[user_name.lower()]
for movie in movie_ratings:
    if movie not in not_watched:
        user_rating = 0
        for rating in movie_ratings[movie]:
            if rating[0] == user_name.lower():
                user_rating = rating[1]
        differences = {}
        for rating in movie_ratings[movie]:
            if rating[0] != user_name.lower():
                difference = abs(rating[1] - user_rating)
                differences[rating[0]] = difference
        for person in differences:
            if differences[person] >= 4:
                weights[person] -= 2
            elif differences[person] >= 2:
                weights[person] -= 1
            elif differences[person] >= 1:
                weights[person] += 1
            else:
                weights[person] += 2

print(f'You are most similar to {gcm([i for i in weights if weights[i] == max(weights.values())][0],
                                     people, 1, 0)[0]}\n')

threshold = 4

if not_watched:
    print('Here is a list of predicted ratings for movies you haven\'t yet watched (Estimate):')
else:
    print('[You would usually be shown predicted ratings, but it seems you have watched all movies from our'
          ' database]')

for order, movie in enumerate(not_watched, start=1):
    others_ratings = []
    using_weights = []
    for rating in movie_ratings[movie]:
        if weights[rating[0]] > threshold:
            using_weights.append(weights[rating[0]])
            others_ratings.append(rating[1])
        using_weights.append(10)
        others_ratings.append(0)
    print(f'{order}. {movie} -', round(weighted_avg(others_ratings, weights=using_weights), 1))

print('\nHere are the scores for how similar people are to you (Estimate):')
ordered_weights = sorted(weights.items(), key=lambda x: x[1])
for order, id in enumerate(ordered_weights, start=1):
    print(f'{order}. {gcm(id[0], people, 1, 0)[0]} ({id[1] / 2})')