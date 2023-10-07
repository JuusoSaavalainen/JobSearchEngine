from testscraper import search_jobs
import string
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
from langdetect import detect
from sklearn.feature_extraction.text import TfidfVectorizer


def get_jobs(keywords:list):
    df = search_jobs(keywords)
    return df


def description_remove_stopwords(description):
    description = description.str.lower()
    stopwords = open("stopwords.txt", "r")
    data = stopwords.read()
    stopwords_list = data.split("\n")
    description.fillna("", inplace=True)
    description = description.apply(lambda x: "".join([c for c in x if c not in string.punctuation]))
    description = description.apply(lambda text: " ".join([word for word in text.split() if word not in stopwords_list]))
    return description


def stem_text(text):
    lang = detect(text)
    stemmer = SnowballStemmer(lang if lang in SnowballStemmer.languages else "english")
    return " ".join([stemmer.stem(word) for word in text.split()])


def stem_description(description):
    description = description.apply(stem_text) 
    return description


def vectorize_description(description) -> spmatrix:
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(description)
    return tfidf_matrix


def clean_description(df):
    description = df["description"]
    description_no_stopwords = description_remove_stopwords(description)
    stemmed_description = stem_description(description_no_stopwords)
    return stemmed_description



def clean_via_search(keywords):
    df = get_jobs(list(keywords))
    description = clean_description(df)
    df["description"] = description
    print(description)
    print(df)
    

def clean_via_csv():
    df = pd.read_csv("wantedjobs.csv")
    description = clean_description(df)
    df["description"] = description
    print(description)
    print(df)



if __name__ == "__main__":
    clean_via_csv()