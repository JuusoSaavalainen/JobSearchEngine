from cleaner import vectorize_description
import pandas as pd


df = pd.read_csv("uniquejobs_clean.csv")
tfidf_matrix=vectorize_description(df["description"])


#calculate similarity score
from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


from sklearn.cluster import AgglomerativeClustering
clustering_model = AgglomerativeClustering(affinity='precomputed', linkage='complete')
clustering_model.fit(cosine_sim)
labels = clustering_model.labels_
df['Cluster'] = labels


def sort_all_jobs(df, cosine_sim):
    sorted_jobs = {}
    for idx, job in df.iterrows():
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sorted_jobs[job['job-title']] = [df.loc[i[0], 'job-title'] for i in sim_scores[1:]]
    return sorted_jobs

print(sort_all_jobs(df,cosine_sim))