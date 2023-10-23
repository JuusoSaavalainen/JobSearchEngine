import string
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
from langdetect import detect
from sklearn.feature_extraction.text import TfidfVectorizer


def description_remove_stopwords(description: pd.DataFrame):
    description = description.str.lower()
    stopwords = open("stopwords.txt", "r")
    data = stopwords.read()
    stopwords_list = data.split("\n")
    description.fillna("", inplace=True)
    description = description.apply(
        lambda x: "".join([c for c in x if c not in string.punctuation])
    )
    description = description.apply(
        lambda text: " ".join(
            [word for word in text.split() if word not in stopwords_list]
        )
    )
    return description


def stem_text(text):
    lang = detect(text)
    stemmer = SnowballStemmer(lang if lang in SnowballStemmer.languages else "english")
    return " ".join([stemmer.stem(word) for word in text.split()])


def stem_description(description: pd.DataFrame):
    description = description.apply(stem_text)
    return description


def vectorize_description(description: pd.DataFrame):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(description)
    return tfidf_matrix


def tokenizer(description: pd.DataFrame):
    description = description.apply(lambda x: x.split(" "))
    return description


def clean_description(df):
    description = df["description"]
    description_no_stopwords = description_remove_stopwords(description)
    stemmed_description = stem_description(description_no_stopwords)
    tokenized_description = tokenizer(stemmed_description)
    df["description"] = tokenized_description
    return df


def lower_df(df: pd.DataFrame):
    description = df["description"]
    description = description.str.lower()
    return df


def clean_df(df: pd.DataFrame):
    """Return cleaned dataframe"""
    description = clean_description(df)
    return description


if __name__ == "__main__":
    df = pd.read_csv("uniquejobs_clean.csv")
    clean_df(df)
