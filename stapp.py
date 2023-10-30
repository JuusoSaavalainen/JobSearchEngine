from bs4 import BeautifulSoup
import requests
import streamlit as st
import requests
import os
import random


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
                job_id = card.find(
                    "div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
                job_id_element = card.find("div", {"class": "base-card"})
            except:
                return "Error in scraping the urn"
            if job_id_element and 'data-entity-urn' in job_id_element.attrs:
                job_entity_urn = job_id_element['data-entity-urn']
                job_id = job_entity_urn.split(":")[3]
                job_ids.append(job_id)
            else:
                print(
                    "Job ID element or data-entity-urn attribute not found for this card.")
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
            job["company"] = soup.find(
                "div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            job["company"] = None
        try:
            job["job-title"] = soup.find(
                "div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
        except:
            job["job-title"] = None
        try:
            job["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find(
                "li").text.replace("Seniority level", "").strip()
        except:
            job["level"] = None
        try:
            job["description"] = soup.find(
                "div", {"class": "show-more-less-html__markup"}).text.strip()
        except:
            job["description"] = None
        try:
            job_url = soup.find(
                "div", {"class": "top-card-layout__entity-info"}).find("a").get("href")
            job_url = job_url.split('?')[0]
            job["job-url"] = job_url
        except:
            job["job-url"] = None
        if any(job.values()):
            jobs.append(job)
    return jobs


API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"


def query(payload):
    key = os.environ.get("API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def main():
    st.markdown("""
        <style>
            .reportview-container {
                background-color: #f0f0f0; 
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.2);
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Job Search Engine</h1>",
                unsafe_allow_html=True)
    keyword = st.text_input("Enter the keyword to search for jobs:")
    if st.button("Search"):
        with st.spinner("Searching for jobs..."):
            job_ids = scrape_job_ids(keyword)
        with st.spinner("Scraping the job descriptions..."):
            job_details = scrape_job_details(job_ids)
        with st.spinner("Evaluating the data..."):
            if job_details:
                job_list = []
                for job in job_details:
                    if "description" in job:
                        description = job["description"]
                        output = query({
                            "inputs": description,
                            "parameters": {"candidate_labels": ["requires job experience", "does not require previous experience"]},
                            "options": {"wait_for_model": True}
                        })
                        if "labels" in output:
                            most_likely_label = output["labels"][0]
                        else:
                            st.write(
                                f"Unexpected keys in output: {output.keys()}")
                            st.write(f"API error: {output['error']}")
                        classification_output = output
                        if most_likely_label == "does not require previous experience":
                            job_list.append({
                                "job-title": job["job-title"],
                                "URL": job["job-url"],
                                "Most Likely Label": most_likely_label,
                                "Model Output": classification_output
                            })
                        if len(job_list) >= 5:
                            break
                random.shuffle(job_list)
                st.header(
                    f"Found these realistic entry-level jobs in Helsinki with keyword: {keyword}")
                st.markdown("---")
                for job in job_list:
                    st.subheader(job["job-title"])
                    st.write("URL:", job["URL"])
                    st.markdown("---")
                if not job_list:
                    st.warning(
                        "No job descriptions found that don't require previous work experience.")
            else:
                st.warning("No jobs found for the given keyword.")


if __name__ == "__main__":
    main()
