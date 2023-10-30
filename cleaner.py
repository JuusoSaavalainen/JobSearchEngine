import string
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
from langdetect import detect
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup


def description_remove_stopwords(df: pd.DataFrame):
    description = df["description"]
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
    return df


def stem_text(text):
    lang = detect(text)
    stemmer = SnowballStemmer(
        lang if lang in SnowballStemmer.languages else "english")
    return " ".join([stemmer.stem(word) for word in text.split()])


def stem_description(df: pd.DataFrame) -> pd.DataFrame:
    description = df["description"]
    description = description.apply(stem_text)
    return df


def vectorize_description(df: pd.DataFrame) -> pd.DataFrame:
    description = df["description"]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(description)
    return tfidf_matrix


def tokenizer(df: pd.DataFrame) -> pd.DataFrame:
    description = df["description"]
    description = description.apply(lambda x: x.split(" "))
    return df


def clean_description(df: pd.DataFrame) -> pd.DataFrame:
    description = df["description"]
    description_no_stopwords = description_remove_stopwords(description)
    stemmed_description = stem_description(description_no_stopwords)
    tokenized_description = tokenizer(stemmed_description)
    df["description"] = tokenized_description
    return df


def lower_description(df: pd.DataFrame) -> pd.DataFrame:
    description = df["description"]
    description = description.str.lower()
    return df


def remove_html_tags(text):
    try:
        if pd.isna(text):
            return text
        return BeautifulSoup(str(text), 'html.parser').get_text()
    except Exception as e:
        print(f"An exception occurred: {e}")
        return None


def clean_html_tags_from_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df["description"] = df["description"].apply(remove_html_tags)
    df.dropna(subset=['description'], inplace=True)
    return df


def read_csv_relevant_columns_inorder(csv_filename: str) -> pd.DataFrame:
    df = pd.read_csv(csv_filename, usecols=[
                     'company', 'job-title', 'level', 'description', 'job-url'])
    return df


if __name__ == "__main__":
    df = pd.read_csv("data_versions/uniquejobs_clean.csv")
    clean_description(df)
