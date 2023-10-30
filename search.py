import pandas as pd
import math
from thefuzz import fuzz

PUNC = '''!()-[]{};:'"\,<>./?@#$%^&*_~+€`’'''

with open("stopwords.txt", encoding="utf8") as f:
    STOPWORDS = f.read().splitlines()


def remove_punc(s: str) -> str:
    for p in PUNC:
        s = s.replace(p, "")
    return s


def tokenize(s: str) -> list:
    s = remove_punc(s)  # Remove punctuation
    s = "".join([c for c in s if not c.isdigit()])
    s = s.lower()
    l = s.split()
    l = [s for s in l if s not in STOPWORDS]
    return l


def match_score(keyword_tokens=list[str], text_tokens=list[str]) -> float:
    """Calculates match score for list of text_tokens for given keyword_tokens"""
    def single_match_score(keyword_token: str):
        total = 0
        for text_token in text_tokens:
            fuzz_match = fuzz.ratio(text_token, keyword_token) / 100
            total += 1 * (fuzz_match > 0.9)
        return total

    scores = math.log(1 + sum(single_match_score(keyword_token)
                      for keyword_token in keyword_tokens))

    return scores


def search_score(raw_data: pd.DataFrame, search_string: str) -> list:
    """Compute search scores for each job post in raw_data"""

    # Tokenize search_string
    keywords = tokenize(search_string)

    # Get title scores
    # Transform titles into token lists
    titles = [tokenize(s) for s in list(raw_data["job_title"])]
    title_scores = [match_score(keywords, x) for x in titles]

    # Get description scores
    descriptions = [tokenize(s) for s in list(raw_data["description"])]
    description_scores = [math.log(1 + match_score(keywords, x))
                          for x in descriptions]

    # Combine scores
    scores = [x + y for x, y in zip(title_scores, description_scores)]

    return scores
