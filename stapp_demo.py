import requests
import streamlit as st
import requests
import os
import pandas as pd
import random

API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"

def query(payload):
    headers = {"Authorization": f"Bearer {st.secrets[API_KEY]}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def get_available_keywords_ordered():
    # Get a list of CSV files in the "data_crawl" folder
    csv_files = [f for f in os.listdir("data_crawl") if f.endswith(".csv")]
    # Extract keywords from file names (remove '.csv' extension)
    keywords = [os.path.splitext(file)[0] for file in csv_files]
    # Order keywords based on DataFrame size (number of rows)
    keywords.sort(key=lambda keyword: len(pd.read_csv(os.path.join("data_crawl", keyword + ".csv"))))
    keywords.reverse()
    return keywords

def main():
    # Add the background card and title
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

    st.markdown("<h1 style='text-align: center;'>Job Search Engine</h1>", unsafe_allow_html=True)

    st.info("This demo app may provide you with an expired link since this version uses static data from linkedin to prevent any issues with scraping. For that reason this app is also limited to fixed size inputs to search for.")

    # Get available keywords ordered by DataFrame size
    keywords = get_available_keywords_ordered()
    selected_keyword = st.selectbox("Select a keyword:", keywords)

    if st.button("Search"):
        with st.spinner("Searching for jobs..."):
            # Construct the file path based on the selected keyword
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

            # Shuffle the job descriptions
            random.shuffle(job_list)

            suitable_jobs_found = 0  # Counter for suitable jobs

            if job_list:
                st.header(f"Realistic {selected_keyword} jobs in Helsinki")
                st.markdown("---")
                for job in job_list:  # Shuffle ensures randomness
                    # Get the description for classification
                    description = job["Description"]
                    
                    # Use the Hugging Face model for classification
                    output = query({
                        "inputs": description,
                        "parameters": {"candidate_labels": ["requires job experience", "does not require previous experience"]},
                        "options": {"wait_for_model": True}
                    })
                    
                    if "labels" in output:
                        most_likely_label = output["labels"][0]
                    else:
                        st.write(f"Unexpected keys in output: {output.keys()}")
                        st.write(f"API error: {output['error']}")
                        most_likely_label = "Error"

                    # Check if the description is suitable (you can adjust the condition)
                    if most_likely_label == "does not require previous experience":
                        st.subheader(job["job-title"])
                        st.write("URL:", job["URL"])
                        st.markdown("---")
                        
                        suitable_jobs_found += 1

                    # Stop searching if 5 suitable jobs are found or we reach the end of the CSV
                    if suitable_jobs_found >= 5 or suitable_jobs_found == len(job_list):
                        break

            if not any(job_list):
                st.warning(f"No matching jobs found for the keyword: {selected_keyword}")

if __name__ == "__main__":
    main()