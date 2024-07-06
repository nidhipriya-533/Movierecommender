import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import os 
import ast 
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

pd.options.mode.chained_assignment = None

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

film = movies.merge(credits,on='title')

filmss = film.drop(['budget',  'homepage', 'id', 'keywords', 'original_language',
       'original_title', 'popularity', 'production_companies',
       'production_countries', 'release_date', 'revenue', 'runtime',
       'spoken_languages', 'status', 'tagline', 'vote_average',
       'vote_count'],axis = 1)

filmss.dropna(inplace=True)

def convert(text):
    l=[]
    for i in ast.literal_eval(text):
        l.append(i['name'])
    return l

filmss['genres']=filmss['genres'].apply(convert)

def convert2(text):
    l=[]
    count = 0
    for i in ast.literal_eval(text):
        if count < 3:
            l.append(i['name'])
        count+=1
    return l

filmss['cast']=filmss['cast'].apply(convert2)

def convert3(text):
    l=[]
    for i in ast.literal_eval(text):
        if i['job']=='Director':
            l.append(i['name'])
            break
    return l

filmss['crew']=filmss['crew'].apply(convert3)
filmss['overview']=filmss['overview'].apply(lambda x:x.split())

def space(word):
    l=[]
    for i  in word:
        l.append(i.replace(" ",""))
    return l

filmss['cast']=filmss['cast'].apply(space)
filmss['crew']=filmss['crew'].apply(space)

filmss['keywords'] = film.keywords
filmss['keywords']=filmss['keywords'].apply(convert)
filmss['keywords']=filmss['keywords'].apply(space)
filmss['genres']=filmss['genres'].apply(space)

filmss['tags']= filmss['overview'] + filmss['genres']+ filmss['keywords'] + filmss['cast'] + filmss['crew']
df = filmss[['movie_id','title','tags']]

df['tags'] = df['tags'].apply(lambda x:' '.join(x))
df['tags'] = df['tags'].apply(lambda x:x.lower())

ps = PorterStemmer()

def stem(text):
    l =[]
    for i in text.split():
        l.append(ps.stem(i))
    return ' '.join(l)

df['tags'] = df['tags'].apply(stem)

cv = CountVectorizer(max_features=5000 , stop_words='english')
vector = cv.fit_transform(df['tags']).toarray()

similar = cosine_similarity(vector)

def recommender(movie):
    index = df[df['title'] == movie].index[0]
    dist = sorted(list(enumerate(similar[index])),reverse=True, key= lambda x: x[1])
    mv = []
    for i in dist[1:6]:
        x= df.iloc[i[0]].title
        mv.append(x)
    return mv

# print(recommender("Pirates"))
##----------------------------------------------------------------------------------------------------------------------------------------------


movie_list = movies['title'].tolist()
import difflib

# Example list of movie names
# movie_list = [
#     "Inception",
#     "Interstellar",
#     "The Dark Knight",
#     "Pulp Fiction",
#     "Avatar",
#     # Add more movie names here
# ]

def find_closest_movie(user_input):
    closest_match = difflib.get_close_matches(user_input, movie_list, n=1)
    if closest_match:
        return closest_match[0]
    else:
        return "No close match found."

# Example usage
# user_movie_input = input("Enter a movie name: ")
# closest_movie = find_closest_movie(user_movie_input)
# print(f"Closest movie: {closest_movie}")

# def vivek(mname):

#     return h

recommendation_dict = {}

# Specify the desired key


# Assign the entire list to the chosen key in the dictionary


# print(recommendation_dict)

from fastapi import FastAPI
from mangum import Mangum

app=FastAPI()
handler= Mangum(app)

@app.get('/')
def endpoint_l():
    output = { 'output':'Hello BY Vivek'}
    return output

@app.get('/hello')
def endpoint_2():
    output = { 'output':'Hello only by api'}
    return output

# @app.get("/movies/{item_id}")
# def get_item(item_id):
#     h = recommender(find_closest_movie(f'{item_id}'))
#     key_name = "Recommendations"
#     recommendation_dict[key_name] = h
#     return recommendation_dict

@app.get("/movies/{item_id}")
def get_item(item_id):
    recommendations = {"Recommendations": recommender(find_closest_movie(f'{item_id}'))}
    return recommendations


  
