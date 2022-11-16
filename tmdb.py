import pandas as pd
import requests
import config

API_KEY=config.api_key

response_list=[]
for movie_id in range(550,556):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, API_KEY)
    r = requests.get(url)
    response_list.append(r.json())


df = pd.DataFrame.from_dict(response_list)
df_columns=['budget', 'id', 'imdb_id', 'original_title', 'release_date', 'revenue', 'runtime']

genres_list=df['genres'].tolist()
flat_list=[item for sublist in genres_list for item in sublist]

result=[]
for i in genres_list:
    r=[]
    for d in i:
        r.append(d['name'])
    result.append(r)
df=df.assign(genres_all=result)

df_genres=pd.DataFrame.from_records(flat_list).drop_duplicates()
df_genres_columns=df_genres['name'].tolist()
df_columns.extend(df_genres_columns)

s=df['genres_all'].explode()
df=df.join(pd.crosstab(s.index,s))
df['release_date']=pd.to_datetime(df['release_date'])
df['day']=df['release_date'].dt.day
df['month']=df['release_date'].dt.month
df['year']=df['release_date'].dt.year
df['day_of_week']=df['release_date'].dt.day_name()

df_times_column=['id', 'release_date', 'day', 'month', 'year', 'day_of_week']
df[df_columns].to_csv('tmbd_movies.csv',index=False)
df_genres.to_csv('tmdb_genres.csv', index=False)
df[df_times_column].to_csv('tmdb_datetimes.csv', index=False)

