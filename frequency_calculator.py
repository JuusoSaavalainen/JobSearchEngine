import pandas as pd
from cleaner import clean_df
from collections import Counter


df = pd.read_csv("data_versions/uniquejobs_clean.csv")
df = clean_df(df)

all_keywords = []
for keywords in df['description']:
    all_keywords.extend(keywords)

keyword_frequency = Counter(all_keywords)
print(keyword_frequency.most_common(300))