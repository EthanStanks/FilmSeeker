import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import spacy
nlp = spacy.load('en_core_web_lg')

SEED = 1292023
CLEAN_DATA = False
PERFORM_EDA = False
TRAIN_MODEL = False

def CleanData():
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

if __name__ == '__main__':
    # Clean Data
    if CLEAN_DATA:
        CleanData()

    # Data Prep
    data = os.path.join('data/','cleaned_movies.csv')
    df = pd.read_csv(data)
    input = df.loc[:,'overview']
    output = df.loc[:,'title']
    stop_words = list(CountVectorizer(stop_words='english').get_stop_words())

    # EDA
    if PERFORM_EDA:
        EDA(input, stop_words)

    # Model
    if TRAIN_MODEL:
        pipeline = Pipeline([
            ('cv', CountVectorizer(lowercase=True, stop_words=stop_words, tokenizer=tokenizer)),
            ('tfidf', TfidfTransformer()),
            ('model', KNeighborsClassifier())
        ])

        X_train, X_test, y_train, y_test = train_test_split(input, output, random_state=SEED)
        pipeline.fit(X_train, y_train)

    