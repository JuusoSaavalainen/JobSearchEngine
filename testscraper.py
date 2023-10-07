from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import asyncio
import aiohttp
import time

def get_user_input():
    search_for = input('Enter the keyword to search for jobs: ')
    return search_for


async def fetch(url:str, headers:str) -> str:
    async with aiohttp.ClientSession() as session:
        await asyncio.sleep(10)  
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Received status code {response.status}")
                return None


async def scrape_job_ids(keywords: list) -> set:
    job_ids = set()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location=Helsinki%2C%20Uusimaa%2C%20Finland&geoId=106591199&f_E=2&start={}'
    # hardcoded 5 page max

    tasks = []
    for keyword in keywords:
        for page_number in range(5):
            url = base_url.format(keyword, page_number * 25)
            task = asyncio.ensure_future(fetch(url, headers))
            tasks.append(task)

    responses = await asyncio.gather(*tasks)
    for response in responses:
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            job_cards = soup.find_all("li")
            for card in job_cards:
                job_id_element = card.find("div", {"class": "base-card"})
                if job_id_element and 'data-entity-urn' in job_id_element.attrs:
                    job_entity_urn = job_id_element['data-entity-urn']
                    job_id = job_entity_urn.split(":")[3]
                    job_ids.add(job_id)
                else:
                    print("Job ID element or data-entity-urn attribute not found for this card.")
    return job_ids


def scrape_job_details(job_ids: list) -> list:
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


def save_to_csv(data: pd.DataFrame):
    data.to_csv('wantedjobs.csv', index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)


def search_jobs(*keywords: str) -> pd.DataFrame:
    job_ids = asyncio.run(scrape_job_ids(list(keywords)))

    job_details = scrape_job_details(job_ids)

    return pd.DataFrame(job_details)

if __name__ == "__main__":
    job_details = search_jobs(
        "devops", 
        "python", 
        "developer",
        "back-end", 
        "front-end",
        "full-stack", 
        "fullstack", 
        "ios", 
        "android",
        "game%20developer",
        "ui/ux",
        "cloud",
        "aws",
        "azure",
        "gcp",
        "data",
        "data%20engineer",
        "data%20analyst",
        "data%20scientist",
        "ml",
        "ai",
        "nlp",
        "cybersecurity",
        "network",
        "qa",
        "test%20engineer",
        "systems%20engineer",
        "embedded",
        "firmware",
        "blockchain",
        "ar/vr",
        "big%20data",
        "dba",
        "rpa",
        "product%20manager"
    )
    save_to_csv(job_details)

