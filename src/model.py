import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
import spacy
nlp = spacy.load('en_core_web_lg')
from sklearn.metrics.pairwise import cosine_similarity
import pickle

CLEAN_DATA = False
PERFORM_EDA = False
TRAIN_MODEL = False
PREDICT_MOVIES = False
NUM_TO_RECOMMEND = 5

def CleanData():
    data = os.path.join('data/','movies.csv')
    output_data = os.path.join('data/','cleaned_movies.csv')
    df = pd.read_csv(data)
    df = df[df['vote_average'] >= 4.5]
    df = df[df['vote_count'] >= 100]
    df = df[df['runtime'] >= 40]
    df = df[df['original_language'] == 'en']
    df = df[df['status'] == 'Released']
    df = df.drop(['id', 'original_language', 'production_companies', 'budget', 'revenue', 'backdrop_path', 'recommendations'
                  ,'credits','status', 'tagline', 'keywords', 'popularity'], axis=1)
    df = df.dropna()
    df['poster_path'] = "https://image.tmdb.org/t/p/w500/" + df['poster_path']
    df.info()
    df.to_csv(output_data, index=False)

def GraphWorldCloud(input, stop_words):
    all_descriptions = ' '.join(input)
    word_cloud = WordCloud(width=800, height=400).generate(all_descriptions)
    if stop_words != None:
        word_cloud = WordCloud(width=800, height=400,stopwords=stop_words).generate(all_descriptions)
    fig, ax = plt.subplots(figsize=(10,5))
    plt.imshow(word_cloud)
    plt.axis("off")
    if stop_words != None:
        plt.title('Word Cloud After Stop Words',fontsize=30)
        plt.savefig(os.path.join('output/','WordCloudAfter.png'))
    else:
        plt.title('Word Cloud Before Stop Words',fontsize=30)
        plt.savefig(os.path.join('output/','WordCloudBefore.png'))
    plt.close()

def EDA(input, stop_words):
    GraphWorldCloud(input, None)
    GraphWorldCloud(input, stop_words)

def tokenizer(text):
    return [token.lemma_ for token in nlp(text)]

def Model(input, stop_words):
    tfidf_vectorizer = Pipeline([
        ('cv', CountVectorizer(lowercase=True, stop_words=stop_words, tokenizer=tokenizer)),
        ('tfidf', TfidfTransformer())
    ])

    tfidf_matrix = tfidf_vectorizer.fit_transform(input)
    with open('data/tfidf_matrix.pkl', 'wb') as file:
        pickle.dump(tfidf_matrix, file)
    with open('data/tfidf_vectorizer.pkl', 'wb') as file:
        pickle.dump(tfidf_vectorizer, file)

def ReadPickle():
    with open('data/tfidf_matrix.pkl', 'rb') as file:
        tfidf_matrix = pickle.load(file)
    with open('data/tfidf_vectorizer.pkl', 'rb') as file:
        tfidf_vectorizer = pickle.load(file)
    return tfidf_matrix, tfidf_vectorizer 

def weighted_rating(x, m, C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

def recommend_movies(user_input, tfidf_matrix, tfidf_vectorizer, df, nums_to_recommend):
    C = df['vote_average'].mean()
    m = df['vote_count'].quantile(0.75)
    df['score'] = df.apply(lambda x: weighted_rating(x, m, C), axis=1)

    user_input_tfidf = tfidf_vectorizer.transform([user_input])
    cos_similarities = cosine_similarity(user_input_tfidf, tfidf_matrix).flatten()
    similarity_df = pd.DataFrame(cos_similarities, columns=['similarity'], index=df.index)

    merged_df = df.merge(similarity_df, left_index=True, right_index=True)
    relevant_movies = merged_df[merged_df['similarity'] >= 0.1]
    sorted_movies = relevant_movies.sort_values(by=['similarity', 'score'], ascending=False)

    recommendations = sorted_movies.head(nums_to_recommend)[['title', 'genres', 'release_date', 'runtime', 'vote_average','vote_count','score','poster_path']].to_dict('records')
    return recommendations

def ReadData():
    data = os.path.join('data/','cleaned_movies.csv')
    df = pd.read_csv(data)
    return df


if __name__ == '__main__':
    # Clean Data
    if CLEAN_DATA:
        CleanData()

    # Data Prep
    df = ReadData()
    if PERFORM_EDA or TRAIN_MODEL:
        input = df.loc[:,'overview']
        stop_words = list(CountVectorizer(stop_words='english').get_stop_words())

    # EDA
    if PERFORM_EDA:
        EDA(input, stop_words)

    # Model
    if TRAIN_MODEL:
        Model(input, stop_words)

    # Predict
    tfidf_matrix, tfidf_vectorizer = ReadPickle()
    recommended_movies = recommend_movies("man finds love", tfidf_matrix,tfidf_vectorizer, df, NUM_TO_RECOMMEND)
    for movie in recommended_movies:
                print(f"{movie['title']} {movie['genres']} {movie['release_date']} {movie['runtime']} {movie['vote_average']} {movie['vote_count']} {movie['score']} {movie['poster_path']}")

    while PREDICT_MOVIES:
        
        selection = input("FilmSeeker\n--------------------------------\nA) Get Recommendation\nB) Exit\nYour selction: ")
        if selection.lower() == 'a':
            os.system('cls')
            print("FilmSeeker\n--------------------------------")
            user_input = input("What would you like to watch?\nInput: ")
            recommended_movies = recommend_movies(user_input, tfidf_matrix, df, NUM_TO_RECOMMEND)
            os.system('cls')
            print(f"FilmSeeker\n--------------------------------\nMovies based on '{user_input}':\n\n")
            for movie in recommended_movies:
                print(f"{movie['title']} {movie['genres']} {movie['release_date']} {movie['runtime']} {movie['score']}")
            print("--------------------------------")
            input("Press any button to continue...")
            os.system('cls')
        elif selection.lower() == 'b':
            PREDICT_MOVIES = False
        else:
            print("Please enter 'A' or 'B' only.")
            input("Press any button to continue...")
            os.system('cls')

    