from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline, AutoTokenizer
import pandas as pd
import requests
import joblib
import streamlit as st


def get_user_input():
    search_for = input('Enter the keyword to search for jobs: ')
    return search_for

def scrape_job_ids(keyword):
    job_ids = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location=Helsinki%2C%20Uusimaa%2C%20Finland&geoId=106591199&f_E=2&start={}'
    # hardcoded 5 page max
    for page_number in range(5):
        url = base_url.format(keyword, page_number * 25)
        response = requests.get(url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all("li")
        for card in job_cards:
            try:
                job_id = card.find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
                job_id_element = card.find("div", {"class": "base-card"})
            except:
                return "Error in scraping the urn"
            if job_id_element and 'data-entity-urn' in job_id_element.attrs:
                job_entity_urn = job_id_element['data-entity-urn']
                job_id = job_entity_urn.split(":")[3]
                job_ids.append(job_id)
            else:
                print("Job ID element or data-entity-urn attribute not found for this card.")
    return job_ids


def scrape_job_details(job_ids):
    jobs = []
    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    for job_id in job_ids:
        url = target_url.format(job_id)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        job = {}
        try:
            job["company"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            job["company"] = None
        try:
            job["job-title"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
        except:
            job["job-title"] = None
        try:
            job["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find("li").text.replace("Seniority level", "").strip()
        except:
            job["level"] = None
        try:
            job["description"] = soup.find("div", {"class": "show-more-less-html__markup"}).text.strip()
        except:
            job["description"] = None
        try:
            job_url = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").get("href")
            job_url = job_url.split('?')[0] 
            job["job-url"] = job_url
        except:
            job["job-url"] = None
        if any(job.values()):
            jobs.append(job)
    return jobs

def make_predictions(model, job_descs):
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    job_descs_tfidf = tfidf_vectorizer.fit_transform(job_descs)
    predictions = model.predict(job_descs_tfidf)
    return predictions


def classify_w_hugging(sequence_to_classify):
    tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
    classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", tokenizer=tokenizer)
    candidate_labels = ["requires previous work experience", "does not require previous work experience"]
    output = classifier(sequence_to_classify, candidate_labels, multi_label=False)
    
    # Find the label with the highest score
    max_score_index = output["scores"].index(max(output["scores"]))
    most_likely_label = output["labels"][max_score_index]
    
    return most_likely_label, output

if __name__ == "__main__":

    st.title("Job Search Engine")
    keyword = st.text_input("Enter the keyword to search for jobs:")

    if st.button("Search"):

        st.info("Searching for jobs...")
        job_ids = scrape_job_ids(keyword)
        st.info("Scraping the descriptions...")
        job_details = scrape_job_details(job_ids)
        st.info("Evaluating the data...")

        if job_details:
            job_list = []
            for job in job_details:
                if "description" in job:
                    description = job["description"]
                    most_likely_label, classification_output = classify_w_hugging(description)
                    if most_likely_label == "does not require previous work experience":
                        job_list.append({
                            "job-title": job["job-title"],
                            "URL": job["job-url"],
                            "Most Likely Label": most_likely_label,
                            "Model Output": classification_output
                        })
                    if len(job_list) >= 5:
                        break
            st.header(f"Found these realistic entry-level jobs in Helsinki with keyword: {keyword}")
            for job in job_list:
                st.subheader(job["job-title"])
                st.write("URL:", job["URL"])
                st.write("Most Likely Label:", job["Most Likely Label"])
                st.write("Model Output:", job["Model Output"])
            if not job_list:
                st.warning("No job descriptions found that don't require previous work experience.")
        else:
            st.warning("No jobs found for the given keyword.")