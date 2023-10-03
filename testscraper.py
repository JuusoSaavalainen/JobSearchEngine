from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_user_input():
    search_for = input('Enter the keyword to search for jobs: ')
    return search_for

def scrape_job_ids(keyword):
    job_ids = []
    base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location=Helsinki%2C%20Uusimaa%2C%20Finland&geoId=106591199&f_E=2&start={}'
    # hardcoded 5 page max
    for page_number in range(5):
        url = base_url.format(keyword, page_number * 25)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all("li")
        for card in job_cards:
            job_id = card.find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
            job_ids.append(job_id)
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
            print(f'Im scraping this job: {job_url}')
        except:
            job["job-url"] = None
        if any(job.values()):
            jobs.append(job)
    return jobs

def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('wantedjobs.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    keyword = get_user_input()
    job_ids = scrape_job_ids(keyword)
    job_details = scrape_job_details(job_ids)
    save_to_csv(job_details)
