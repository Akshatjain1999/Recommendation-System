import pandas as pd
import numpy as np
import random 
from collections import defaultdict
import re

class MovieGenres:
    def __init__(self):
        self.movies = pd.read_csv('../ml-latest-small/movies.csv')
        self.rating = pd.read_csv('../ml-latest-small/ratings.csv')
        self.list_of_genre=set()
        self.users=set()
        self.movies_by_gen = defaultdict(list)
        self.movies['genres'] = self.movies.genres.str.split('|')
        
        for gen in self.movies.genres:
            for i in gen:
                if i!='(no genres listed)':
                    self.list_of_genre.add(i)
        def split_genre(val):
            try:
                if g in val:
                    return 1
                else:
                    return 0
            except AttributeError:
                return 0
        for g in self.list_of_genre:
            self.movies[g] = self.movies.genres.apply(split_genre) 
              
        for i in self.rating['userId'].values:
            self.users.add(i)

        
        
    def movie_by_genre(self,genre='Action'):
        
        temp = pd.merge(self.movies,self.rating,on='movieId')
        temp = pd.DataFrame(temp.groupby('movieId')['rating'].mean()).reset_index()
        # print(temp)
        new_df = pd.merge(self.movies,temp,on='movieId')
        # print(new_df)
        for g in self.list_of_genre:
            self.movies_by_gen[g]= list(new_df[(new_df[g]==1) & (new_df['rating']>=3.5)].title.values)
            
        results =  random.choices(self.movies_by_gen[genre],k=10)
        for i,j in enumerate(results):
            p = re.compile(r"(?:\((\d{4})\))?\s*$")
            results[i]=p.sub("",j)
        return results
    

