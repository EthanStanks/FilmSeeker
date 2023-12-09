import os
import pandas as pd

def DataPrep():
    data = os.path.join('data/','movies.csv')
    output_data = os.path.join('data/','cleaned_movies.csv')
    df = pd.read_csv(data)
    df = df[df['original_language'] == 'en']
    df = df[df['status'] == 'Released']
    df = df.drop(['id', 'original_language', 'production_companies', 'budget', 'revenue', 'backdrop_path', 'recommendations',
                   'poster_path', 'credits','status', 'tagline', 'keywords', 'vote_count', 'popularity'], axis=1)
    df = df.dropna()
    df.info()
    df.to_csv(output_data, index=False)

if __name__ == '__main__':
    # Data Prep
    data = os.path.join('data/','cleaned_movies.csv')
    df = pd.read_csv(data)
    df.info()
    input = df.loc[:,'overview']
    ouput = df.loc[:,'title']
    