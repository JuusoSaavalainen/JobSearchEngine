from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
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

if __name__ == "__main__":
    st.title("Job Search Engine")

    # User input for job search keyword
    keyword = st.text_input("Enter the keyword to search for jobs:")

    if st.button("Search"):
        st.info("Searching for jobs...")

        # Scrape job IDs and details
        job_ids = scrape_job_ids(keyword)
        st.info("Scraping the descriptions...")
        job_details = scrape_job_details(job_ids)
        st.info("Evaluating the data...")
        if job_details:
            model = joblib.load("best_model.pkl")

            # Extract job descriptions and make predictions
            job_descs = [job["description"] for job in job_details if "description" in job]
            if job_descs:
                predictions = make_predictions(model, job_descs)

                # Display the first 5 job titles and URLs for labeled 0
                st.header(f"Found these (limit = 5) realistic entry level jobs in Helsinki with keyword: {keyword}")
                printed_count = 0
                for i in range(len(job_details)):
                    if predictions[i] == 0:
                        st.subheader(job_details[i]["job-title"])
                        st.markdown(f"**URL:** [Link]({job_details[i]['job-url']})")
                        printed_count += 1
                    if printed_count == 5:
                        break
            else:
                st.warning("No job descriptions found in the scraped data.")
        else:
            st.warning("No jobs found for the given keyword.")