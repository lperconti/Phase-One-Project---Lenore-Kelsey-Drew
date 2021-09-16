import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('white')



def top_5_genres(clean_data):

    clean_data_high_rating = clean_data[clean_data['averagerating'] >= 8]

    split_genres = clean_data.assign(genres=clean_data_high_rating.genres.str.split(',')).explode('genres')
        
    top_5_genres_high_rating = split_genres['genres'].value_counts()[:5]

    x = top_5_genres_high_rating.index
    y = top_5_genres_high_rating

    data={'Genres': x,
          'Num. of Movies within Category': y}
        
    df = pd.DataFrame(data)

    plt.figure(figsize=(10,6))
    chart = sns.barplot(x='Genres', y='Num. of Movies within Category', data=df)
    for p in chart.patches:
        chart.annotate("%.0f" % p.get_height(), 
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                        textcoords='offset points')

    chart.set_title('Top 5 Genres that Produced the Highest Ratings')

    return chart



def top_10_directors_drama(imdb, imdb_name_basics_slim):
    
    #Splits genres into the top two highest rated
    split_genres = imdb.assign(genres=imdb.genres.str.split(",")).explode('genres')

    drama_imdb = split_genres[split_genres['genres'] == 'Drama']
    action_imdb = split_genres[split_genres['genres'] == 'Action']
    
    #Splits up any entry with multiple directors to single rows and merges with name_basics
    split_directors = drama_imdb.assign(directors=drama_imdb.directors.str.split(",")).explode('directors')
    to_be_or_not = split_directors.merge(imdb_name_basics_slim, left_on = 'directors', right_on = 'nconst')
    to_be_or_not.head()

    #Gets rid of any dead directors
    alive_imdb_directors = to_be_or_not[to_be_or_not['death_year'].isna()]

    # Sort only directors who've directed three or more drama films in the last five years
    top_directors = alive_imdb_directors.groupby('primary_name')['tconst'].count().sort_values(ascending = False)
    top_directors_names = top_directors[top_directors.values > 2]
    names_list = list(top_directors_names.index.values)
    imdb_top_directors = alive_imdb_directors[alive_imdb_directors['primary_name'].isin(names_list)]
    
    top_directors = imdb_top_directors.groupby('primary_name')['averagerating'].mean().sort_values(ascending = False)[:10]
    
    plt.figure(figsize=(10,6))

    director_drama_data = {'Directors': top_directors.index,
                           'Average Rating': top_directors.values}
    df_director_drama = pd.DataFrame(director_drama_data)
    directors_drama = sns.barplot(x='Directors', y='Average Rating', data=df_director_drama)
    directors_drama.set_title('Directors Who Have the Highest Average Rating in the Drama Genre - Directed 3+ Movies')

    #rotates x-tick labels
    directors_drama.set_xticklabels(labels=director_drama_data['Directors'], rotation = 30)

    #Pushes labels to left to match with correct bar after rotating
    plt.setp(directors_drama.xaxis.get_majorticklabels(), ha='right')

    #Adds total labels to bars
    for p in directors_drama.patches:
        directors_drama.annotate(format(p.get_height(), '.1f'), 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                 ha = 'center', va = 'center', 
                                 xytext = (0, 9), 
                                 textcoords = 'offset points')
    
    return directors_drama

def runtime_minutes(imdb):
    imdb_split_genres = imdb.assign(genres=imdb.genres.str.split(",")).explode('genres')

    dramas = imdb_split_genres[(imdb_split_genres['genres'] == 'Drama')]
    dramas_runtimes_mean = dramas['runtime_minutes'].mean()

    action = imdb_split_genres[(imdb_split_genres['genres'] == 'Action')]
    action_runtimes_mean = action['runtime_minutes'].mean()

    genre_dict = {'Genres': ['Action', 'Drama'],
                  'Runtimes (min)': [action_runtimes_mean, dramas_runtimes_mean]}

    df_genre_runtimes = pd.DataFrame(genre_dict)

    plt.figure(figsize=(10, 6))

    genre_runtimes = sns.barplot(x='Genres', y='Runtimes (min)', data=df_genre_runtimes)
    genre_runtimes.set_title('Drama and Action Runtimes for Highly Rated Movies')

    #Adds total labels to bars
    for p in genre_runtimes.patches:
        genre_runtimes.annotate(format(p.get_height(), '.1f'), 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                ha = 'center', va = 'center', 
                                xytext = (0, 9),                 
                                textcoords = 'offset points')

    return genre_runtimes


def directors_average_rating(imdb, imdb_name_basics_slim):
    #Splits genres into the top two highest rated
    split_genres = imdb.assign(genres=imdb.genres.str.split(",")).explode('genres')

    drama_imdb = split_genres[split_genres['genres'] == 'Drama']
    action_imdb = split_genres[split_genres['genres'] == 'Action']
    
    #Splits up any entry with multiple directors to single rows and merges with name_basics
    split_directors = drama_imdb.assign(directors=drama_imdb.directors.str.split(",")).explode('directors')
    to_be_or_not = split_directors.merge(imdb_name_basics_slim, left_on = 'directors', right_on = 'nconst')
    to_be_or_not.head()

    #Gets rid of any dead directors
    alive_imdb_directors = to_be_or_not[to_be_or_not['death_year'].isna()]

    # Sort only directors who've directed three or more drama films in the last five years
    top_directors = alive_imdb_directors.groupby('primary_name')['tconst'].count().sort_values(ascending = False)
    top_directors_names = top_directors[top_directors.values > 2]
    names_list = list(top_directors_names.index.values)
    imdb_top_directors = alive_imdb_directors[alive_imdb_directors['primary_name'].isin(names_list)]
    
    top_directors = imdb_top_directors.groupby('primary_name')['averagerating'].mean().sort_values(ascending = False)

    plt.figure(figsize = (10, 6))

    directors_average = sns.lineplot(x = top_directors.index, y = top_directors.values, marker = 'o')
    directors_average.set_title('Writers Of Multiple Action Films Vs Their Average Movie Rating')
    directors_average.set_ylabel('Average Rating')
    directors_average.axes.get_xaxis().set_ticks([])
    directors_average.set_xlabel('Directors')

    return directors_average