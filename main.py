import pandas as pd
import search
import job_level

def load_data() -> pd.DataFrame:
    """Load raw job post data"""
    df = pd.read_csv("data_versions/uniquejobs.csv")
    df.rename(columns={"job-title": "job_title", "job-url": "job_url"}, inplace=True)
    return df

def total_score(search_scores: list, level_scores: list) -> list:
    assert len(search_scores) == len(level_scores)
    return [x + y for x, y in zip(search_scores, level_scores)]


if __name__ == "__main__":

    # Load raw data: DataFrame of job ads
    raw_data = load_data()

    # Get "search relevance" scores for each job post
    search_scores = search.search_score(raw_data, input("Search string: "))

    # Get "entry levelness" scores for each job post
    level_scores = list(job_level.level_score(raw_data)["entry_level_score"])

    # Scale both scores
    def scale_scores(scores: list) -> list:
        max_score = max(scores)
        scores = [x / max_score for x in scores]
        return scores
    search_scores, level_scores = scale_scores(search_scores), scale_scores(level_scores)

    # Get total scores
    total_scores = total_score(search_scores, level_scores)
    
    # Sort job ads based on score
    # High score = good; low score = bad
    raw_data["score"] = total_scores
    raw_data["score_search"] = search_scores
    raw_data["score_level"] = level_scores
    raw_data.sort_values(by="score", ascending=False, inplace=True)

    # Show top-5 URLs just for fun and giggles
    # TODO: do something more meaningful here once we have an actual logic for scores
    for url in raw_data["job_url"][:5]:
        print(url)

    # Optional: print to test output file
    #raw_data.to_csv("data_versions/TEST_output.csv")
