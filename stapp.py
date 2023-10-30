from bs4 import BeautifulSoup
import requests
import streamlit as st
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
            #description_div = soup.find("div", {"class": "show-more-less-html__markup"})
            #job["job-details"] = BeautifulSoup(description_div, 'html.parser').prettify()
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
                background-color: linear-gradient(135deg, #f5f5f5, #e0e0e0); 
                padding: 20px 15px;
                border-radius: 12px;
                box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.15);
            }
            .reportview-container:hover {
                transform: translateY(-2px); 
                box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.25), 0 8px 24px 0 rgba(0, 0, 0, 0.2); 
            }
            .title {
                color: black;
                font-family: 'Arial', sans-serif; 
                font-size: 18px;  
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                max-width: 90%;  
                margin-top: 8px;
                margin-bottom: 4px;
                transition: color 0.3s ease;
                }
            .title:hover {
                color: #555; 
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
                            classification_output = output
                            most_likely_label = output["labels"][0] 
                            if most_likely_label == "does not require previous experience":
                                job_list.append({
                                    "job-title": job["job-title"],
                                    "URL": job["job-url"],
                                    "description": job["description"],
                                    "Most Likely Label": most_likely_label,
                                    "Model Output": classification_output
                                })
                        else:
                            st.error(f"Unexpected keys in output: {output.keys()} \n API error: {output['error']}")
                            break
                        if len(job_list) >= 5:
                            break
                random.shuffle(job_list)
                st.header(
                    f"Found these realistic entry-level jobs in Helsinki with keyword: {keyword}")
                st.markdown("---")    
                for job in job_list:
                    job_title = job["job-title"]
                    job_url = job["URL"]
                    job_details = job["description"]
                    st.markdown(
                        f"""
                        <div class="reportview-container">
                            <a href="{job_url}" target="_blank">
                                <div class="title">{job_title}</div>
                            </a>
                            <details>{job_details}
                            </details>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                if not job_list:
                    st.warning(
                        "No job descriptions found that don't require previous work experience.")
            else:
                st.warning("No jobs found for the given keyword.")


if __name__ == "__main__":
    main()
