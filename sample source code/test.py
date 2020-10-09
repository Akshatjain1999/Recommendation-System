import recommender as r
rec = r.Recommender()
rec.fit(reviews_pth='train_data.csv', movies_pth= 'movies_clean.csv', learning_rate=.005, iters=20)
ids , movies = rec.make_recommendations(19869,'user')
for i in movies:
    print(i)
