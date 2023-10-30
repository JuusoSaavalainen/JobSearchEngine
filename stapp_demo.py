import requests
import streamlit as st
import requests
import os
import pandas as pd
import random

API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"

def query(payload):
    key = st.secrets["API_KEY"]
    headers = {"Authorization": f"Bearer {key}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def get_available_keywords_ordered():
    csv_files = [f for f in os.listdir("data_crawl") if f.endswith(".csv")]
    keywords = [os.path.splitext(file)[0] for file in csv_files]
    keywords.sort(key=lambda keyword: len(pd.read_csv(os.path.join("data_crawl", keyword + ".csv"))))
    keywords.reverse()
    return keywords

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
    st.markdown("<h1 style='text-align: center;'>Job Search Engine</h1>", unsafe_allow_html=True)
    st.info("This demo app may provide you with an expired link since this version uses static data to prevent any issues with scraping. For that reason this app is also limited to fixed size inputs to search for.")
    keywords = get_available_keywords_ordered()
    selected_keyword = st.selectbox("Select a keyword:", keywords)

    if st.button("Search"):
        with st.spinner("Searching for jobs..."):
            file_path = os.path.join("data_crawl", selected_keyword + ".csv")
            if not os.path.exists(file_path):
                st.warning(f"No CSV file found for the keyword: {selected_keyword}")
                return
            df = pd.read_csv(file_path)
            job_list = []
            for index, row in df.iterrows():
                job_list.append({
                    "job-title": row['job-title'],
                    "URL": row['job-url'],
                    "Description": row['description']
                })
            random.shuffle(job_list)
            suitable_jobs_found = 0
            if job_list:
                st.header(f"Realistic Entry level {selected_keyword} jobs in Helsinki")
                st.markdown("---")
                for job in job_list:
                    description = job["Description"]
                    output = query({
                        "inputs": description,
                        "parameters": {"candidate_labels": ["requires job experience", "does not require previous experience"]},
                        "options": {"wait_for_model": True}
                    })
                    if "labels" in output:
                        most_likely_label = output["labels"][0]
                        if most_likely_label == "does not require previous experience":
                            job_title = job["job-title"]
                            job_url = job["URL"]
                            st.markdown(
                            f"""
                            <div class="reportview-container">
                                <a href="{job_url}" target="_blank">
                                    <div class="title">{job_title}</div>
                                </a>
                                <details>{description}
                                </details>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        st.write(f"Unexpected keys in output: {output.keys()}")
                        st.write(f"API error: {output['error']}")
                        most_likely_label = "Error"
                    
                    if suitable_jobs_found >= 5 or suitable_jobs_found == len(job_list):
                        break
            if not any(job_list):
                st.warning(f"No matching jobs found for the keyword: {selected_keyword}")
if __name__ == "__main__":
    main()

