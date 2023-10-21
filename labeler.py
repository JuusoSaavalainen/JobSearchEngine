import openai
openai.api_key = "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"
from cleaner import clean_via_csv

def label(job_desciption: str) -> bool:
    
    prompt = f"""
    Label the following job description as either 'realistic' or 'unrealistic':
    
    Example: Entry-level job description: 'No experience required, training provided'
    Label: realistic
    
    Entry-level job description: {job_desciption}
    Label:
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"user","content":prompt}
            ],
    )
    
    return response

def label_dataframe(df):
    df["label"] = df["description"].apply(label)
    df.to_csv("labeled.csv")
    
    
if __name__ == "__main__":
    df = clean_via_csv("uniquejobs.csv")
    df.to_csv("uniquejobs_clean.csv")