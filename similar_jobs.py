from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from cleaner import vectorize_description
import pandas as pd


df = pd.read_csv("data_versions/uniquejobs_clean.csv")
tfidf_matrix = vectorize_description(df["description"])


# calculate similarity score
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


clustering_model = AgglomerativeClustering(
    affinity='precomputed', linkage='complete')
clustering_model.fit(cosine_sim)
labels = clustering_model.labels_
df['Cluster'] = labels
