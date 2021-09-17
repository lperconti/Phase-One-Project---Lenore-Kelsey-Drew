#data manipulation packages
import pandas as pd

#visualization packages
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('white')


#displays a graph of the top 5 genres produced with high ratings
def top_5_genres(imdb):

    #takes the movies with high ratings
    high_rating = imdb[imdb['averagerating'] >= 8]

    #splits their genres
    split_genres = imdb.assign(genres=high_rating.genres.str.split(',')).explode('genres')
        
    #finds the top five most produced genres
    top_5_genres_high_rating = split_genres['genres'].value_counts()[:5]

    #form data that pandas can read
    data = {'Genres': top_5_genres_high_rating.index,
            'Num. of Movies within Category': top_5_genres_high_rating}
        
    #creates a dataframe from the data
    df = pd.DataFrame(data)

    #sizes the figure
    plt.figure(figsize=(10,6))

    #plots the figure
    chart = sns.barplot(x='Genres', y='Num. of Movies within Category', data=df)

    #decorations
    for p in chart.patches:
        chart.annotate("%.0f" % p.get_height(), 
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                        textcoords='offset points')

    chart.set_title('Top 5 Genres that Produced the Highest Ratings')

    return chart


#displays graph of the top 10 directors of drama
def top_10_directors_drama(imdb, imdb_name_basics_slim):
    
    #Splits genres of each movie
    split_genres = imdb.assign(genres=imdb.genres.str.split(",")).explode('genres')

    #isolates drama
    drama_imdb = split_genres[split_genres['genres'] == 'Drama']
    
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
    
    #sorts the top directors
    top_directors = imdb_top_directors.groupby('primary_name')['averagerating'].mean().sort_values(ascending = False)[:10]
    

    #forms data for pandas to read
    director_drama_data = {'Directors': top_directors.index,
                           'Average Rating': top_directors.values}

    #creates a dataframe from that data
    df_director_drama = pd.DataFrame(director_drama_data)

    #sizes figure
    plt.figure(figsize=(10,6))

    #plots figure
    directors_drama = sns.barplot(x='Directors', y='Average Rating', data=df_director_drama)

    #decorations
    directors_drama.set_title('Directors Who Have the Highest Average Rating in the Drama Genre - Directed 3+ Movies')

    directors_drama.set_xticklabels(labels=director_drama_data['Directors'], rotation = 30)

    plt.setp(directors_drama.xaxis.get_majorticklabels(), ha='right')

    #Adds total labels to bars
    for p in directors_drama.patches:
        directors_drama.annotate(format(p.get_height(), '.1f'), 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                 ha = 'center', va = 'center', 
                                 xytext = (0, 9), 
                                 textcoords = 'offset points')
    
    return directors_drama


#displays average runtime minutes of the top 2 genres
def runtime_minutes(imdb):

    #splits the genres of the movies
    imdb_split_genres = imdb.assign(genres=imdb.genres.str.split(",")).explode('genres')

    #isolates drama
    dramas = imdb_split_genres[(imdb_split_genres['genres'] == 'Drama')]
    dramas_runtimes_mean = dramas['runtime_minutes'].mean()

    #isolates action
    action = imdb_split_genres[(imdb_split_genres['genres'] == 'Action')]
    action_runtimes_mean = action['runtime_minutes'].mean()

    #forms data for pandas to read
    genre_dict = {'Genres': ['Action', 'Drama'],
                  'Runtimes (min)': [action_runtimes_mean, dramas_runtimes_mean]}

    #creates dataframe of data
    df_genre_runtimes = pd.DataFrame(genre_dict)

    #sizes figure
    plt.figure(figsize=(10, 6))

    #plots figure
    genre_runtimes = sns.barplot(x='Genres', y='Runtimes (min)', data=df_genre_runtimes)

    #decorations
    genre_runtimes.set_title('Drama and Action Runtimes for Highly Rated Movies')

    for p in genre_runtimes.patches:
        genre_runtimes.annotate(format(p.get_height(), '.1f'), 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                ha = 'center', va = 'center', 
                                xytext = (0, 9),                 
                                textcoords = 'offset points')

    return genre_runtimes


#displays 
def directors_average_rating(imdb, imdb_name_basics_slim):

    #Splits the genres of the movies
    split_genres = imdb.assign(genres=imdb.genres.str.split(",")).explode('genres')

    #isolates drama
    drama_imdb = split_genres[split_genres['genres'] == 'Drama']
    
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
    
    #takes all directors
    top_directors = imdb_top_directors.groupby('primary_name')['averagerating'].mean().sort_values(ascending = False)

    #sizes the figure
    plt.figure(figsize = (10, 6))

    #plots figure
    directors_average = sns.lineplot(x = top_directors.index, y = top_directors.values, marker = 'o')

    #decorations
    directors_average.set_title('Writers Of Multiple Action Films Vs Their Average Movie Rating')
    directors_average.set_ylabel('Average Rating')
    directors_average.axes.get_xaxis().set_ticks([])
    directors_average.set_xlabel('Directors')

    return directors_average